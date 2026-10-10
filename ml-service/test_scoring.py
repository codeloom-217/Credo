
import os
import sys
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from app.features import extract_features
from app.scoring import CredoScoringModel

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "gigworker-transaction-data.csv"
)

df = pd.read_csv(DATA_PATH)

features = extract_features(df)

scoring_model = CredoScoringModel()

results = scoring_model.predict_score(features)

print(
    results[
        [
            "customer_id",
            "credo_score",
            "risk_band",
            "predicted_outcome",
            "predicted_probability"
        ]
    ].head(10)
)

print("\nRisk band distribution:")
print(results["risk_band"].value_counts())

print("\nScoring test completed.")
