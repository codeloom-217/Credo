
import pandas as pd

from app.momentum import calculate_momentum


def create_transactions(incomes, expenses):
    records = []

    dates = pd.date_range(
        start="2026-01-01",
        periods=6,
        freq="MS"
    )

    for date, income, expense in zip(dates, incomes, expenses):
        records.append({
            "transaction_date": date,
            "amount": income,
            "transaction_type": "CREDIT"
        })

        records.append({
            "transaction_date": date,
            "amount": expense,
            "transaction_type": "DEBIT"
        })

    return pd.DataFrame(records)


def test_improving_momentum():
    transactions = create_transactions(
        incomes=[10000, 10000, 10000, 12000, 12000, 12000],
        expenses=[9000, 9000, 9000, 7000, 7000, 7000]
    )

    result = calculate_momentum(transactions)

    assert result["momentum"] == "IMPROVING"


def test_declining_momentum():
    transactions = create_transactions(
        incomes=[12000, 12000, 12000, 10000, 10000, 10000],
        expenses=[7000, 7000, 7000, 9000, 9000, 9000]
    )

    result = calculate_momentum(transactions)

    assert result["momentum"] == "DECLINING"


def test_insufficient_data():
    transactions = pd.DataFrame({
        "transaction_date": ["2026-06-01"],
        "amount": [10000],
        "transaction_type": ["CREDIT"]
    })

    result = calculate_momentum(transactions)

    assert result["momentum"] == "NEED_REVIEW"
    assert result["momentum_change_percent"] is None


def test_missing_required_columns():
    transactions = pd.DataFrame({
        "transaction_date": ["2026-06-01"],
        "amount": [10000]
    })

    result = calculate_momentum(transactions)

    assert result["momentum"] == "NEED_REVIEW"
    assert result["momentum_change_percent"] is None
