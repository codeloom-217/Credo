
import os
import joblib
import numpy as np
import pandas as pd


class CredoScoringModel:
    def __init__(self):
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "models",
            "credo_model.pkl"
        )

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"CREDO model file not found: {model_path}"
            )

        saved_data = joblib.load(model_path)

        if not isinstance(saved_data, dict):
            raise ValueError(
                "Invalid model file: expected a dictionary."
            )

        required_keys = {"model", "threshold", "model_features"}
        missing_keys = required_keys - saved_data.keys()

        if missing_keys:
            raise ValueError(
                f"Invalid model file. Missing keys: {sorted(missing_keys)}"
            )

        self.model = saved_data["model"]
        self.threshold = 0.51
        self.model_features = saved_data["model_features"]

        if not hasattr(self.model, "predict_proba"):
            raise TypeError(
                "The loaded model does not support predict_proba()."
            )

        if not 0 <= self.threshold <= 1:
            raise ValueError(
                "The saved threshold must be between 0 and 1."
            )

        if not self.model_features:
            raise ValueError("The saved model feature list is empty.")

    def predict_score(self, features: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(features, pd.DataFrame):
            raise TypeError("Features must be a pandas DataFrame.")

        if features.empty:
            raise ValueError("No customer features were provided.")

        missing_features = [
            column
            for column in self.model_features
            if column not in features.columns
        ]

        if missing_features:
            raise ValueError(
                f"Missing required features: {missing_features}"
            )

        X = features.loc[:, self.model_features].copy()
        X = X.apply(pd.to_numeric, errors="coerce")

        if not np.isfinite(X.to_numpy(dtype=float)).all():
            raise ValueError(
                "Features contain missing, non-numeric, or infinite values."
            )

        class_labels = list(self.model.classes_)

        if 1 not in class_labels:
            raise ValueError(
                "The trained model does not contain positive class 1."
            )

        probabilities = self.model.predict_proba(X)
        positive_class_index = class_labels.index(1)
        probabilities = probabilities[:, positive_class_index]

        result = features.copy()

        result["credo_score"] = (
            probabilities * 100
        ).round().astype(int).clip(1, 100)

        result["risk_band"] = result["credo_score"].apply(
            self._risk_band
        )

        result["predicted_outcome"] = (
            probabilities >= self.threshold
        ).astype(int)

        result["predicted_probability"] = probabilities

        return result

    @staticmethod
    def _risk_band(score):
        if score >= 71:
            return "Low"
        elif score >= 41:
            return "Moderate"
        else:
            return "High"
