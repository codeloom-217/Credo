
import pandas as pd


def calculate_momentum(transactions: pd.DataFrame) -> dict:
    required_columns = {"transaction_date", "amount", "transaction_type"}

    if not required_columns.issubset(transactions.columns):
        return {
            "momentum": "Insufficient Data",
            "momentum_change_percent": None
        }

    data = transactions.copy()
    data["transaction_date"] = pd.to_datetime(
        data["transaction_date"], errors="coerce"
    )
    data["amount"] = pd.to_numeric(data["amount"], errors="coerce")

    data = data.dropna(
        subset=["transaction_date", "amount", "transaction_type"]
    )

    if data.empty:
        return {
            "momentum": "Insufficient Data",
            "momentum_change_percent": None
        }

    data["transaction_month"] = (
        data["transaction_date"].dt.to_period("M")
    )

    monthly_activity = data.groupby("transaction_month").size()

    if len(monthly_activity) < 2:
        return {
            "momentum": "Insufficient Data",
            "momentum_change_percent": None
        }

    recent_activity = monthly_activity.iloc[-1]
    previous_activity = monthly_activity.iloc[-2]

    if previous_activity == 0:
        change_percent = None
        momentum = "Insufficient Data"
    else:
        change_percent = round(
            ((recent_activity - previous_activity) / previous_activity) * 100,
            2
        )

        if change_percent > 5:
            momentum = "Improving"
        elif change_percent < -5:
            momentum = "Declining"
        else:
            momentum = "Stable"

    return {
        "momentum": momentum,
        "momentum_change_percent": change_percent
    }
