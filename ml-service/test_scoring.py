
import pandas as pd

from app.features import extract_features
from app.scoring import CredoScoringModel

df = pd.read_csv("data/gigworker-transaction-data.csv")

features = extract_features(df)

model = CredoScoringModel()

result = model.predict_score(features)

print(
    result[
        ["customer_id", "credo_score", "risk_band"]
    ].head(5)
)