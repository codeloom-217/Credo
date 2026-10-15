
import pandas as pd
import numpy as np


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["balance"] = pd.to_numeric(
        df["balance"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "customer_id",
            "transaction_date",
            "amount",
            "balance"
        ]
    )

    df["credit_amount"] = np.where(
        df["transaction_type"] == "CREDIT",
        df["amount"],
        0
    )

    df["debit_amount"] = np.where(
        df["transaction_type"] == "DEBIT",
        df["amount"],
        0
    )

    df["transaction_month"] = (
        df["transaction_date"].dt.to_period("M")
    )

    features = df.groupby("customer_id").agg(
        total_income=("credit_amount", "sum"),
        average_income=("credit_amount", "mean"),
        income_transaction_count=("credit_amount", lambda x: (x > 0).sum()),

        total_expense=("debit_amount", "sum"),
        average_expense=("debit_amount", "mean"),
        expense_transaction_count=("debit_amount", lambda x: (x > 0).sum()),

        average_balance=("balance", "mean"),
        minimum_balance=("balance", "min"),
        maximum_balance=("balance", "max"),

        transaction_count=("amount", "count"),

        income_volatility=("credit_amount", "std"),
        expense_volatility=("debit_amount", "std"),

        mode_diversity=("transaction_mode", "nunique"),
        transaction_type_diversity=("transaction_type", "nunique"),
    ).reset_index()

    monthly_activity = (
        df.groupby(["customer_id", "transaction_month"])
        .size()
        .groupby("customer_id")
        .mean()
        .rename("average_monthly_transactions")
    )

    features = features.merge(
        monthly_activity,
        on="customer_id",
        how="left"
    )

    features["expense_to_income_ratio"] = np.where(
        features["total_income"] > 0,
        features["total_expense"] / features["total_income"],
        0
    )

    features["savings_rate"] = np.where(
        features["total_income"] > 0,
        (
            features["total_income"]
            - features["total_expense"]
        ) / features["total_income"],
        0
    )

    features["income_volatility"] = (
        features["income_volatility"].fillna(0)
    )

    features["expense_volatility"] = (
        features["expense_volatility"].fillna(0)
    )

    return features
