import streamlit as st
import requests
import pandas as pd

st.title("Demand Forecasting")

mode = st.radio("Select Mode", ["Single Date", "Date Range"])

if mode == "Single Date":
    date = st.date_input("Select Date")
    promo = st.selectbox("Promo", [0, 1])

    if st.button("Predict"):
        try:
            response = requests.get(
                "http://127.0.0.1:8000/predict",
                params={"date": str(date), "promo": promo}
            )
            data = response.json()
            st.success(f"Predicted Sales: {round(data['predicted_sales'], 2)}")
        except:
            st.error("API not running")

else:
    start = st.date_input("Start Date")
    end = st.date_input("End Date")
    promo = st.selectbox("Promo (applied to all days)", [0, 1])

    if st.button("Predict Range"):
        try:
            response = requests.get(
                "http://127.0.0.1:8000/predict_range",
                params={
                    "start": str(start),
                    "end": str(end),
                    "promo": promo
                }
            )

            data = response.json()

            df = pd.DataFrame(data)

            st.subheader("Predictions")
            st.dataframe(df)

            st.subheader("Sales Trend")
            st.line_chart(df.set_index("date")["predicted_sales"])

            st.subheader("Summary")
            st.write("Total Sales:", round(df["predicted_sales"].sum(), 2))
            st.write("Average Sales:", round(df["predicted_sales"].mean(), 2))
            st.write("Peak Day:", df.loc[df["predicted_sales"].idxmax()]["date"])

        except:
            st.error("API not running")