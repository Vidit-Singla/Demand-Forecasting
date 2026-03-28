import pandas as pd
import pickle

with open("models/prophet_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict(date, promo):
    df = pd.DataFrame({
        "ds": [pd.to_datetime(date)],
        "promo": [promo]
    })
    forecast = model.predict(df)
    return float(forecast["yhat"].iloc[0])

def predict_range(start, end, promo):
    dates = pd.date_range(start=start, end=end)
    df = pd.DataFrame({
        "ds": dates,
        "promo": [promo] * len(dates)
    })
    forecast = model.predict(df)
    return [
        {
            "date": str(df["ds"].iloc[i].date()),
            "predicted_sales": float(forecast["yhat"].iloc[i])
        }
        for i in range(len(df))
    ]