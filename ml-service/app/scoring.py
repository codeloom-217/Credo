
import os
import joblib
import numpy as np
import pandas as pd


class CredoScoringModel:

    def __init__(self):
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "models",
            "credo_model.pkl"
        )

        self.model = joblib.load(model_path)

        self.model_features = [
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

    def predict_score(self, features: pd.DataFrame) -> pd.DataFrame:

        missing_features = [
            column
            for column in self.model_features
            if column not in features.columns
        ]

        if missing_features:
            raise ValueError(
                f"Missing required features: {missing_features}"
            )

        X = features[self.model_features].copy()

        X = X.apply(pd.to_numeric, errors="coerce")

        if not np.isfinite(X.to_numpy(dtype=float)).all():
            raise ValueError(
                "Features contain missing, non-numeric, or infinite values."
            )

        probabilities = self.model.predict_proba(X)[:, 1]

        result = features.copy()

        result["credo_score"] = (
            probabilities * 100
        ).round().astype(int).clip(1, 100)

        result["risk_band"] = result["credo_score"].apply(
            self._risk_band
        )

        result["predicted_outcome"] = (
            probabilities >= 0.5
        ).astype(int)

        result["predicted_probability"] = probabilities

        return result

    def _risk_band(self, score):

        if score >= 71:
            return "Low"

        if score >= 41:
            return "Moderate"

        return "High"
