
import os
import sys
import joblib
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from app.features import extract_features

DATA_PATH = os.path.join(
    BASE_DIR, "data", "gigworker-transaction-data.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR, "models", "credo_model.pkl"
)

RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
features = extract_features(df)

saved_data = joblib.load(MODEL_PATH)
model = saved_data["model"]

model_features = saved_data.get(
    "model_features",
    list(model.feature_names_in_)
)

importance = pd.DataFrame({
    "feature": model_features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance", ascending=False
)

print("\nFeature Importance Ranking")
print(importance.to_string(index=False))

importance.to_csv(
    os.path.join(RESULTS_DIR, "feature_importance.csv"),
    index=False
)

plt.figure(figsize=(10, 6))
plt.barh(
    importance["feature"][::-1],
    importance["importance"][::-1]
)
plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.title("CREDO Random Forest Feature Importance")
plt.tight_layout()

plt.savefig(
    os.path.join(RESULTS_DIR, "feature_importance.png"),
    dpi=300
)

plt.show()
