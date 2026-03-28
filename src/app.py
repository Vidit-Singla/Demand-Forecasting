from fastapi import FastAPI
from predict import predict, predict_range

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Demand Forecasting API is running"}

@app.get("/predict")
def get_prediction(date: str, promo: int):
    return {
        "date": date,
        "promo": promo,
        "predicted_sales": predict(date, promo)
    }

@app.get("/predict_range")
def get_range(start: str, end: str, promo: int):
    return predict_range(start, end, promo)