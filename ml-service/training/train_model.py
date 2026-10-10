
import os
import sys
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
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


# --------------------------------------------------
# 2. LOAD TRANSACTION DATA
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("Transaction rows:", len(df))

features = extract_features(df)

print("Customers:", len(features))


# --------------------------------------------------
# 3. SELECT MODEL FEATURES
# --------------------------------------------------

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


# --------------------------------------------------
# 4. GENERATE SYNTHETIC OUTCOMES
# --------------------------------------------------
# These are simulated labels, not actual loan
# repayment records.

rng = np.random.default_rng(42)

# Savings behavior: map approximately to 0-1
savings_signal = (
    X["savings_rate"].clip(-1, 1) + 1
) / 2

# Lower expense burden produces a higher signal
expense_signal = 1 - (
    X["expense_to_income_ratio"].clip(0, 2) / 2
)

# Balance compared with approximate monthly income
monthly_income = X["total_income"] / 6

balance_coverage = (
    X["average_balance"]
    / monthly_income.replace(0, np.nan)
).replace([np.inf, -np.inf], np.nan).fillna(0)

balance_signal = balance_coverage.clip(0, 2) / 2

# Lower relative income volatility produces
# a higher stability signal
relative_volatility = (
    X["income_volatility"]
    / X["average_income"].replace(0, np.nan)
).replace([np.inf, -np.inf], np.nan).fillna(0)

stability_signal = 1 / (
    1 + relative_volatility.clip(0, 100)
)

# Combine the four behavior signals
behavior_score = (
    0.35 * savings_signal
    + 0.25 * expense_signal
    + 0.25 * balance_signal
    + 0.15 * stability_signal
)

y = (behavior_score >= 0.50).astype(int)
y.name = "synthetic_outcome"

noise_mask = rng.random(len(y)) < 0.10
y.loc[noise_mask] = 1 - y.loc[noise_mask]

print("\nSynthetic Outcome Distribution:")
print(y.value_counts().sort_index())

print("\nClass proportions:")
print(y.value_counts(normalize=True).sort_index())

if y.nunique() != 2:
    raise ValueError(
        "Both synthetic outcome classes are required."
    )

if y.value_counts().min() < 5:
    raise ValueError(
        "Too few customers in one class for reliable "
        "stratified splitting and cross-validation."
    )

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)

print("\nTraining customers:", len(X_train))
print("Validation customers:", len(X_val))
print("Testing customers:", len(X_test))


rf = RandomForestClassifier(
    random_state=42,
    n_jobs=1
)

parameter_grid = {
    "n_estimators": [200, 300, 400, 500],
    "max_depth": [4, 6, 8, 12, None],
    "min_samples_split": [2, 5, 10, 20],
    "min_samples_leaf": [2, 5, 10, 20],
    "max_features": ["sqrt", 0.8, 1.0],
    "class_weight": [None, "balanced"]
}

search = RandomizedSearchCV(
    estimator=rf,
    param_distributions=parameter_grid,
    n_iter=40,
    scoring="accuracy",
    cv=5,
    random_state=42,
    n_jobs=-1,
    refit=True
)

print("\nSearching for the best Random Forest model...")

search.fit(X_train, y_train)

model = search.best_estimator_

print("\nBest parameters:")
print(search.best_params_)

print(
    "Best cross-validation accuracy:",
    round(search.best_score_, 4)
)


train_predictions = model.predict(X_train)

train_accuracy = accuracy_score(
    y_train,
    train_predictions
)

print(
    "\nTraining Accuracy:",
    round(train_accuracy, 4)
)


val_probabilities = model.predict_proba(X_val)[:, 1]

best_threshold = 0.50
best_val_accuracy = -1

for threshold in np.arange(0.30, 0.71, 0.01):

    val_predictions = (
        val_probabilities >= threshold
    ).astype(int)

    current_accuracy = accuracy_score(
        y_val,
        val_predictions
    )

    if current_accuracy > best_val_accuracy:
        best_val_accuracy = current_accuracy
        best_threshold = threshold

print("\nSelected threshold:", round(best_threshold, 2))

print(
    "Validation Accuracy:",
    round(best_val_accuracy, 4)
)

probabilities = model.predict_proba(X_test)[:, 1]

predictions = (
    probabilities >= best_threshold
).astype(int)

accuracy = accuracy_score(y_test, predictions)

print("\nTesting Accuracy:", round(accuracy, 4))
print(f"Testing Accuracy Percentage: {accuracy * 100:.2f}%")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
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


roc_auc = roc_auc_score(y_test, probabilities)

print("\nROC-AUC Score:", round(roc_auc, 4))

fpr, tpr, roc_thresholds = roc_curve(
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


model_path = os.path.join(
    MODEL_DIR, "credo_model.pkl"
)

joblib.dump(
    {
        "model": model,
        "threshold": best_threshold,
        "model_features": model_features
    },
    model_path
)

print("\nModel and threshold saved:", model_path)

print(
    "Confusion matrix saved:",
    os.path.join(RESULTS_DIR, "confusion_matrix.png")
)

print(
    "ROC curve saved:",
    os.path.join(RESULTS_DIR, "roc_curve.png")
)

print("\nTraining and evaluation complete.")

