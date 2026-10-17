
from pydantic import BaseModel, Field
from typing import List


class Transaction(BaseModel):
    customer_id: str = Field(min_length=1)
    transaction_date: str
    transaction_type: str
    amount: float = Field(ge=0)
    balance: float
    transaction_mode: str
    narration: str


class ScoreRequest(BaseModel):
    transactions: List[Transaction] = Field(min_length=1)


class CustomerScore(BaseModel):
    customer_id: str
    credo_score: int = Field(ge=1, le=100)
    risk_band: str
    predicted_outcome: int = Field(ge=0, le=1)
    predicted_probability: float = Field(ge=0, le=1)


class ScoreResponse(BaseModel):
    status: str
    results: List[CustomerScore]
