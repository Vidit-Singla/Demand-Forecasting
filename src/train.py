import pandas as pd
from prophet import Prophet
import pickle

train_df = pd.read_csv("data/train.csv", parse_dates=["Date"])
store = pd.read_csv("data/store.csv")

df = train_df.merge(store, on="Store", how="left")

df = df[df["Store"] == 1].copy()
df = df.sort_values("Date")

df = df[["Date", "Sales", "Promo"]]

df = df.rename(columns={
    "Date": "ds",
    "Sales": "y",
    "Promo": "promo"
})

holidays = pd.DataFrame({
    "holiday": "generic_holiday",
    "ds": pd.to_datetime([
        "2013-12-25", "2014-12-25", "2015-12-25",
        "2013-01-01", "2014-01-01", "2015-01-01"
    ]),
    "lower_window": 0,
    "upper_window": 1
})

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    holidays=holidays
)

model.add_regressor("promo")

model.fit(df)

with open("models/prophet_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully.")