import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

st.title("🔮 Future Unemployment Prediction")

# Load Data
df = pd.read_csv("Unemployment in India.csv")

# Clean Columns
df.columns = df.columns.str.strip()

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# Monthly Average
monthly = (
    df.groupby("Date")
    ["Estimated Unemployment Rate (%)"]
    .mean()
    .reset_index()
)

# Create Time Index
monthly["Month_Index"] = np.arange(len(monthly))

# Train Model
X = monthly[["Month_Index"]]
y = monthly["Estimated Unemployment Rate (%)"]

model = LinearRegression()
model.fit(X, y)

# Predict Future 6 Months
future_months = np.arange(
    len(monthly),
    len(monthly) + 6
).reshape(-1, 1)

predictions = model.predict(future_months)

# Prediction Table
future_df = pd.DataFrame({
    "Future Month": [
        "Month 1",
        "Month 2",
        "Month 3",
        "Month 4",
        "Month 5",
        "Month 6"
    ],
    "Predicted Rate (%)": predictions
})

st.subheader("📈 Next 6 Months Prediction")

st.dataframe(future_df)

# Chart
fig = px.line(
    future_df,
    x="Future Month",
    y="Predicted Rate (%)",
    markers=True,
    title="Predicted Unemployment Trend"
)

st.plotly_chart(fig, use_container_width=True)

# Latest Prediction
st.metric(
    "Expected Unemployment After 6 Months",
    f"{round(predictions[-1],2)}%"
)