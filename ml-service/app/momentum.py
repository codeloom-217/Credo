
import pandas as pd
import numpy as np


def calculate_momentum(transactions: pd.DataFrame) -> dict:
    required_columns = {
        "transaction_date",
        "amount",
        "transaction_type"
    }

    insufficient_data = {
        "momentum": "NEED_REVIEW",
        "momentum_change_percent": None
    }

    if not required_columns.issubset(transactions.columns):
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
        data["transaction_type"].astype(str).str.upper().str.strip()
    )

    data = data.dropna(
        subset=["transaction_date", "amount"]
    )

    data = data[
        data["transaction_type"].isin(["CREDIT", "DEBIT"])
        & (data["amount"] >= 0)
    ]

    if data.empty:
        return insufficient_data

    latest_month = data["transaction_date"].max().to_period("M")
    first_month = latest_month - 5

    data = data[
        data["transaction_date"].dt.to_period("M").between(
            first_month, latest_month
        )
    ]

    monthly_count = data.groupby(
        data["transaction_date"].dt.to_period("M")
    ).size()

    monthly_count = monthly_count.reindex(
        pd.period_range(first_month, latest_month, freq="M"),
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

    data["month"] = data["transaction_date"].dt.to_period("M")

    monthly_features = data.groupby("month").agg(
        income=("income", "sum"),
        expense=("expense", "sum")
    )

    monthly_features = monthly_features.reindex(
        pd.period_range(first_month, latest_month, freq="M"),
        fill_value=0
    )

    previous = monthly_features.iloc[:3]
    recent = monthly_features.iloc[3:]

    def calculate_indicators(period):
        total_income = period["income"].sum()
        total_expense = period["expense"].sum()

        savings_rate = (
            (total_income - total_expense) / total_income
            if total_income > 0 else None
        )

        income_mean = period["income"].mean()
        income_std = period["income"].std(ddof=0)

        income_consistency = (
            max(0, 1 - (income_std / income_mean))
            if income_mean > 0 else None
        )

        expense_ratio = (
            total_expense / total_income
            if total_income > 0 else None
        )

        return {
            "savings_rate": savings_rate,
            "income_consistency": income_consistency,
            "expense_ratio": expense_ratio
        }

    previous_metrics = calculate_indicators(previous)
    recent_metrics = calculate_indicators(recent)

    if any(
        value is None
        for metrics in [previous_metrics, recent_metrics]
        for value in metrics.values()
    ):
        return insufficient_data

    changes = {
        "savings_rate": (
            recent_metrics["savings_rate"]
            - previous_metrics["savings_rate"]
        ),
        "income_consistency": (
            recent_metrics["income_consistency"]
            - previous_metrics["income_consistency"]
        ),
        "expense_ratio": (
            previous_metrics["expense_ratio"]
            - recent_metrics["expense_ratio"]
        )
    }

    weights = {
        "savings_rate": 0.40,
        "income_consistency": 0.30,
        "expense_ratio": 0.30
    }

    momentum_index = sum(
        changes[feature] * weights[feature]
        for feature in weights
    )

    momentum_change_percent = round(
        momentum_index * 100, 2
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
