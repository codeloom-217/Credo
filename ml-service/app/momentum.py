
import pandas as pd
import numpy as np


def calculate_momentum(transactions: pd.DataFrame) -> dict:
    insufficient_data = {
        "momentum": "NEED_REVIEW",
        "momentum_change_percent": None
    }

    required_columns = {
        "transaction_date",
        "amount",
        "transaction_type"
    }

    if (
        not isinstance(transactions, pd.DataFrame)
        or transactions.empty
        or not required_columns.issubset(transactions.columns)
    ):
        return insufficient_data

    data = transactions.copy()

    data["transaction_date"] = pd.to_datetime(
        data["transaction_date"],
        errors="coerce"
    )

    data["amount"] = pd.to_numeric(
        data["amount"],
        errors="coerce"
    )

    data["transaction_type"] = (
        data["transaction_type"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    data = data.dropna(
        subset=["transaction_date", "amount"]
    )

    data = data[
        data["transaction_type"].isin(["CREDIT", "DEBIT"])
        & (data["amount"] >= 0)
        & np.isfinite(data["amount"])
    ]

    if data.empty:
        return insufficient_data

    latest_month = data["transaction_date"].max().to_period("M")
    first_month = latest_month - 5

    month_range = pd.period_range(
        first_month,
        latest_month,
        freq="M"
    )

    data["month"] = data["transaction_date"].dt.to_period("M")

    data = data[
        data["month"].isin(month_range)
    ]

    monthly_count = data.groupby("month").size().reindex(
        month_range,
        fill_value=0
    )

    if (monthly_count == 0).any():
        return insufficient_data

    data["income"] = np.where(
        data["transaction_type"] == "CREDIT",
        data["amount"],
        0
    )

    data["expense"] = np.where(
        data["transaction_type"] == "DEBIT",
        data["amount"],
        0
    )

    monthly_features = data.groupby("month").agg(
        income=("income", "sum"),
        expense=("expense", "sum")
    ).reindex(month_range, fill_value=0)

    previous = monthly_features.iloc[:3]
    recent = monthly_features.iloc[3:]

    def calculate_indicators(period):
        total_income = period["income"].sum()
        total_expense = period["expense"].sum()

        if total_income <= 0:
            return None

        savings_rate = (
            total_income - total_expense
        ) / total_income

        income_mean = period["income"].mean()
        income_std = period["income"].std(ddof=0)

        income_consistency = (
            max(0, 1 - (income_std / income_mean))
            if income_mean > 0 else None
        )

        return {
            "savings_rate": savings_rate,
            "income_consistency": income_consistency
        }

    previous_metrics = calculate_indicators(previous)
    recent_metrics = calculate_indicators(recent)

    if previous_metrics is None or recent_metrics is None:
        return insufficient_data

    if any(
        value is None or not np.isfinite(value)
        for metrics in [previous_metrics, recent_metrics]
        for value in metrics.values()
    ):
        return insufficient_data

    savings_rate_change = (
        recent_metrics["savings_rate"]
        - previous_metrics["savings_rate"]
    )

    income_consistency_change = (
        recent_metrics["income_consistency"]
        - previous_metrics["income_consistency"]
    )

    weights = {
        "savings_rate": 0.70,
        "income_consistency": 0.30
    }

    momentum_index = (
        savings_rate_change * weights["savings_rate"]
        + income_consistency_change * weights["income_consistency"]
    )

    momentum_change_percent = round(
        momentum_index * 100,
        2
    )

    if momentum_change_percent > 2:
        momentum = "IMPROVING"
    elif momentum_change_percent < -2:
        momentum = "DECLINING"
    else:
        momentum = "NEED_REVIEW"

    return {
        "momentum": momentum,
        "momentum_change_percent": momentum_change_percent
    }
