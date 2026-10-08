import os
import joblib
import pandas as pd


class CredoScoringModel:

    def __init__(self):
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "models",
            "credo_model.pkl"
        )

        self.model = joblib.load(model_path)

    def predict_score(self, features: pd.DataFrame) -> pd.DataFrame:
        result = features.copy()

        probabilities = self.model.predict_proba(
            features[self._model_features()]
        )[:, 1]

        result["credo_score"] = (
            probabilities * 100
        ).round().astype(int)

        result["credo_score"] = (
            result["credo_score"]
            .clip(1, 100)
        )

        result["risk_band"] = result["credo_score"].apply(
            self._risk_band
        )

        return result

    def _risk_band(self, score):
        if score >= 71:
            return "Low"

        if score >= 41:
            return "Moderate"

        return "High"

    def _model_features(self):
        return [
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