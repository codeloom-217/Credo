import os
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

from app.features import extract_features


df = pd.read_csv("data/gigworker-transaction-data.csv")

features = extract_features(df)

features["repayment_outcome"] = (
    (features["savings_rate"] >= 0.15)
    & (features["expense_to_income_ratio"] <= 0.80)
    & (features["average_balance"] >= 5000)
).astype(int)

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

X = features[model_features]
y = features["repayment_outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Model Accuracy:", accuracy)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions
    )
)

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/credo_model.pkl"
)

print("\nModel saved successfully!")
print("Location: models/credo_model.pkl")