from fastapi import FastAPI

app = FastAPI(title="CREDO ML Service")


@app.get("/")
def home():
    return {"message": "CREDO ML Service is running"}


@app.post("/score")
def score():
    return {
        "score": 75,
        "risk_band": "MEDIUM"
    }