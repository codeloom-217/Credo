
import os
import joblib
import pandas as pd


class CredoScoringModel:

    def __init__(self):
        # Find the saved model file
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "models",
            "credo_model.pkl"
        )

        # Load the trained model and its settings
        saved_data = joblib.load(model_path)

        self.model = saved_data["model"]
        self.threshold = saved_data["threshold"]

        # Use saved feature names when available
        self.model_features = saved_data.get(
            "model_features",
            list(self.model.feature_names_in_)
        )

    def predict_score(self, features: pd.DataFrame) -> pd.DataFrame:

        # Check that all required features are present
        missing_features = [
            column
            for column in self.model_features
            if column not in features.columns
        ]

        if missing_features:
            raise ValueError(
                f"Missing required features: {missing_features}"
            )

        # Select features in the exact training order
        X = features[self.model_features].copy()

        # Reject invalid numeric input
        X = X.apply(pd.to_numeric, errors="coerce")

        if X.isna().any().any():
            raise ValueError(
                "Features contain missing or non-numeric values."
            )

        if not X.map(
            lambda column: column != float("inf")
            and column != float("-inf")
        ).all().all():
            raise ValueError(
                "Features contain infinite values."
            )

        # Predict probability of synthetic class 1
        probabilities = self.model.predict_proba(X)[:, 1]

        # Preserve the original feature data
        result = features.copy()

        # Convert probability into a score from 1 to 100
        result["credo_score"] = (
            probabilities * 100
        ).round().astype(int).clip(1, 100)

        # Assign a risk band
        result["risk_band"] = result["credo_score"].apply(
            self._risk_band
        )

        # Predict the class using the tuned threshold
        result["predicted_outcome"] = (
            probabilities >= self.threshold
        ).astype(int)

        # Keep the raw model probability for debugging
        result["predicted_probability"] = probabilities

        return result

    def _risk_band(self, score):

        if score >= 71:
            return "Low"

        if score >= 41:
            return "Moderate"

        return "High"
