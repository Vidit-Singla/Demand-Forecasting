# Retail Sales Demand Forecasting

Predicts daily store sales using time series models, served via a FastAPI backend and a Streamlit dashboard. Built on the [Rossmann Store Sales](https://www.kaggle.com/c/rossmann-store-sales) dataset.

---

## What this project does

Retail stores need to know tomorrow's sales *today* — for staffing, stock ordering, and promotions. This project builds a forecasting pipeline that goes from raw historical data all the way to a live prediction API you can query by date.

---

## Project Structure

```
demand-forecasting/
├── data/
│   ├── store.csv
│   ├── sample_submission.csv
│   └── README.md               
├── models/                     # prophet_model.pkl saved here after running train.py
├── notebooks/
│   ├── Data_Interpretation.ipynb   
│   ├── Baselines.ipynb            
│   ├── prophet.ipynb               
│   ├── sarimax.ipynb              
├── src/
│   ├── train.py               
│   ├── predict.py             
│   └── app.py                 
├── ui/
│   └── app.py                  
├── requirements.txt
└── README.md
```

---

## Stack

| Layer | Tool |
|---|---|
| Modelling | Prophet, SARIMAX (statsmodels), scikit-learn |
| Backend API | FastAPI |
| Dashboard | Streamlit |
| Serialisation | pickle |

---

## Models & Results

All models trained on Store #1, 80/20 chronological split.

| Model | MAE | RMSE | MAPE |
|---|---|---|---|
| Seasonal Naive (lag-7) | 1204 | 1701 | 28.6% |
| Linear Regression | 741 | 1147 | 14.1% |
| SARIMAX(1,0,1)(1,1,1)[7] | **544** | 982 | 10.8% |
| Prophet + Promo + Holidays | 559 | **949** | **10.3%** |


The three advanced models all land around **10% MAPE** — roughly 2.7× better than the naive baseline. Prophet is deployed in the API; SARIMAX is the strongest on MAE.

---

## ML Concepts Covered

**EDA & Feature Engineering** — time feature extraction (day-of-week, month, week-of-year), promo effect analysis (avg sales jump from ~5,900 to ~8,200 on promo days), seasonality visualisation.

**Stationarity** — Augmented Dickey-Fuller test to decide whether differencing is needed before ARIMA modelling.

**Baselines** — seasonal naive (lag-7) and linear regression with lag features establish a performance floor that every "real" model must beat.

**Lag features** — `lag_7` and `lag_14` encode weekly autocorrelation directly as input features for the regression model.

**SARIMAX** — classical state-space model with AR(1), MA(1), weekly seasonal differencing (D=1, s=7), and `Promo` as an exogenous regressor.

**Prophet** — additive decomposition model (trend + weekly + yearly seasonality), with Christmas/New Year holidays and `Promo` as an extra regressor.

**Evaluation** — MAE (interpretable in currency units), RMSE (penalises large errors), MAPE (scale-free); zero-sales days excluded from MAPE to avoid division distortion.

---

## Why Accurate Forecasts Matter in Retail

A 10% MAPE on ~€5,000 average daily sales means forecasts are off by ~€500/day. The naive baseline is off by ~€1,430/day. That €930 gap per store per day directly affects three decisions made before the store opens:

- **Inventory** — how much stock to order so shelves aren't empty or overfull
- **Staffing** — how many people to schedule based on expected footfall
- **Promotions** — whether yesterday's promo actually lifted sales above what was already predicted

The prediction API makes this actionable: any downstream system can hit `/predict_range` to get a sales forecast for the coming week before those decisions are locked in.
