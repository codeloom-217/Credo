
import os
import pandas as pd
import matplotlib.pyplot as plt

from app.features import extract_features

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR, "data", "gigworker-transaction-data.csv"
)

RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
features = extract_features(df)

model_features = [
    "total_income",
    "average_income",
    "income_transaction_count",
    "total_expense",
    "average_expense",
    "expense_transaction_count",
    "average_balance",
    "minimum_balance",
    "maximum_balance",
    "transaction_count",
    "income_volatility",
    "expense_volatility",
    "expense_to_income_ratio",
    "savings_rate"
]

X = features[model_features].apply(
    pd.to_numeric, errors="coerce"
)

X = X.replace([float("inf"), float("-inf")], float("nan"))
X = X.dropna()

correlation = X.corr()

print("\nFeature Correlation Matrix:")
print(correlation.round(2).to_string())

high_correlations = []

for i in range(len(model_features)):
    for j in range(i + 1, len(model_features)):
        value = correlation.iloc[i, j]

        if abs(value) >= 0.90:
            high_correlations.append({
                "feature_1": model_features[i],
                "feature_2": model_features[j],
                "correlation": round(value, 3)
            })

print("\nHighly Correlated Feature Pairs (|r| >= 0.90):")

if high_correlations:
    for pair in high_correlations:
        print(pair)
else:
    print("No feature pairs crossed the 0.90 threshold.")

correlation.to_csv(
    os.path.join(RESULTS_DIR, "feature_correlation.csv")
)

plt.figure(figsize=(12, 10))

plt.imshow(
    correlation,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    aspect="auto"
)

plt.colorbar(label="Correlation")
plt.xticks(
    range(len(model_features)),
    model_features,
    rotation=90
)
plt.yticks(range(len(model_features)), model_features)

plt.title("CREDO Feature Correlation Matrix")
plt.tight_layout()

plt.savefig(
    os.path.join(RESULTS_DIR, "feature_correlation.png"),
    dpi=300
)

plt.show()
