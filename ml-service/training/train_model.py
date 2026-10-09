
import os
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_auc_score,
    roc_curve
)

from app.features import extract_features


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "gigworker-transaction-data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")


df = pd.read_csv(DATA_PATH)

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

if y.nunique() != 2:
    raise ValueError(
        "Training requires both outcome classes: 0 and 1."
    )

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
probabilities = model.predict_proba(X_test)[:, 1]

print("Model Accuracy:", accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))

cm = confusion_matrix(y_test, predictions, labels=[0, 1])

print("\nConfusion Matrix:")
print(cm)

roc_auc = roc_auc_score(y_test, probabilities)
print("\nROC-AUC Score:", round(roc_auc, 4))

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

joblib.dump(model, os.path.join(MODEL_DIR, "credo_model.pkl"))

ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=[0, 1]
).plot()

plt.title("CREDO Confusion Matrix")
plt.tight_layout()
plt.savefig(
    os.path.join(RESULTS_DIR, "confusion_matrix.png"),
    dpi=300
)
plt.close()

fpr, tpr, thresholds = roc_curve(y_test, probabilities)

plt.figure()
plt.plot(fpr, tpr, label=f"Random Forest (AUC = {roc_auc:.3f})")
plt.plot([0, 1], [0, 1], linestyle="--", label="Random Classifier")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("CREDO ROC Curve")
plt.legend()
plt.tight_layout()
plt.savefig(
    os.path.join(RESULTS_DIR, "roc_curve.png"),
    dpi=300
)
plt.close()

print("\nModel saved: models/credo_model.pkl")
print("Confusion matrix saved: results/confusion_matrix.png")
print("ROC curve saved: results/roc_curve.png")