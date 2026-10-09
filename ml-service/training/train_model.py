
import os
import sys

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_auc_score,
    roc_curve
)


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, BASE_DIR)

from app.features import extract_features

DATA_PATH = os.path.join(
    BASE_DIR, "data", "gigworker-transaction-data.csv"
)

MODEL_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

print("Transaction rows:", len(df))

features = extract_features(df)

print("Customers:", len(features))

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

X = features[model_features].copy()


X = X.replace([np.inf, -np.inf], np.nan)


X = X.fillna(X.median())


rng = np.random.default_rng(42)


savings_rank = X["savings_rate"].rank(pct=True)

balance_rank = X["average_balance"].rank(pct=True)

expense_rank = X["expense_to_income_ratio"].rank(pct=True)

volatility_rank = X["income_volatility"].rank(pct=True)



behavior_signal = (
    0.40 * savings_rank
    + 0.30 * balance_rank
    - 0.20 * expense_rank
    - 0.10 * volatility_rank
)


logit = 8 * (behavior_signal - behavior_signal.mean())

repayment_probability = 1 / (1 + np.exp(-logit))

y = pd.Series(
    rng.binomial(1, repayment_probability),
    index=X.index,
    name="synthetic_outcome"
)

print("\nSynthetic Outcome Distribution:")
print(y.value_counts().sort_index())
print("\nClass proportions:")
print(y.value_counts(normalize=True).sort_index())

if y.nunique() != 2:
    raise ValueError(
        "Both synthetic outcome classes are required."
    )


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining customers:", len(X_train))
print("Testing customers:", len(X_test))


rf = RandomForestClassifier(
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

parameter_grid = {
    "n_estimators": [100, 200],
    "max_depth": [4, 8, None],
    "min_samples_leaf": [5, 10, 20],
    "max_features": ["sqrt", 0.8]
}

search = GridSearchCV(
    estimator=rf,
    param_grid=parameter_grid,
    scoring="accuracy",
    cv=5,
    n_jobs=-1,
    refit=True
)

print("\nTuning Random Forest...")

search.fit(X_train, y_train)

model = search.best_estimator_

print("\nBest parameters:")
print(search.best_params_)

print(
    "Best cross-validation accuracy:",
    round(search.best_score_, 4)
)



predictions = model.predict(X_test)

probabilities = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, predictions)

print("\nTest Accuracy:", round(accuracy, 4))
print(f"Test Accuracy Percentage: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

cm = confusion_matrix(
    y_test,
    predictions,
    labels=[0, 1]
)

print("\nConfusion Matrix:")
print(cm)

roc_auc = roc_auc_score(y_test, probabilities)

print("\nROC-AUC Score:", round(roc_auc, 4))


model_path = os.path.join(
    MODEL_DIR, "credo_model.pkl"
)

joblib.dump(model, model_path)

print("\nModel saved:", model_path)


ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=[0, 1]
).plot()

plt.title("CREDO Synthetic Outcome - Confusion Matrix")
plt.tight_layout()

plt.savefig(
    os.path.join(RESULTS_DIR, "confusion_matrix.png"),
    dpi=300
)

plt.close()

# --------------------------------------------------
# 10. Save ROC curve
# --------------------------------------------------

fpr, tpr, thresholds = roc_curve(
    y_test,
    probabilities
)

plt.figure()

plt.plot(
    fpr,
    tpr,
    label=f"Random Forest (AUC = {roc_auc:.3f})"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random baseline"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("CREDO Synthetic Outcome - ROC Curve")
plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(RESULTS_DIR, "roc_curve.png"),
    dpi=300
)

plt.close()

print("Confusion matrix saved.")
print("ROC curve saved.")
print("\nTraining and evaluation complete.")