
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd

from app.features import extract_features
from app.scoring import CredoScoringModel

app = FastAPI(
    title="CREDO ML Service",
    description="Alternative credit scoring and underwriting API",
    version="1.0.0"
)

scoring_model = CredoScoringModel()

class Transaction(BaseModel):
    customer_id: str
    transaction_date: str
    transaction_type: str
    amount: float
    balance: float
    transaction_mode: str
    narration: str

class ScoreRequest(BaseModel):
    transactions: List[Transaction]

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
            [transaction.model_dump()
             for transaction in request.transactions]
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

        
        return {
            "status": "success",
            "results": results.to_dict(orient="records")
        }

    except HTTPException:
        raise

    except (ValueError, KeyError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while scoring."
        )
