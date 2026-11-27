
import traceback

import pandas as pd
from fastapi import FastAPI, HTTPException

from app.schemas import ScoreRequest
from app.features import extract_features
from app.scoring import CredoScoringModel
from app.momentum import calculate_momentum


app = FastAPI(
    title="CREDO ML Service",
    description="Alternative credit scoring and underwriting API",
    version="1.0.0"
)

scoring_model = CredoScoringModel()


@app.get("/")
def home():
    return {
        "message": "CREDO ML Service is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "CREDO ML Service"
    }


@app.post("/score")
def score(request: ScoreRequest):
    try:
        transaction_data = pd.DataFrame(
            [
                transaction.model_dump()
                for transaction in request.transactions
            ]
        )

        if transaction_data.empty:
            raise HTTPException(
                status_code=400,
                detail="At least one transaction is required."
            )

        features = extract_features(transaction_data)

        if features.empty:
            raise HTTPException(
                status_code=400,
                detail="No valid customer features could be extracted."
            )

        results = scoring_model.predict_score(features)

        result_records = results.to_dict(orient="records")

        for result in result_records:
            customer_id = result["customer_id"]

            customer_transactions = transaction_data[
                transaction_data["customer_id"] == customer_id
            ]

            momentum_result = calculate_momentum(
                customer_transactions
            )

            result.update(momentum_result)

        return {
            "status": "success",
            "results": result_records
        }

    except HTTPException:
        raise

    except (ValueError, KeyError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while scoring."
        )
