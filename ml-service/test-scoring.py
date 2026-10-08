import pandas as pd

from app.features import extract_features


df = pd.read_csv("data/transactions.csv")

features = extract_features(df)

print(features.head(10))