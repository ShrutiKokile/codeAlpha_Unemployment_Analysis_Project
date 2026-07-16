import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🦠 COVID-19 Impact Analysis")

# Load Dataset
df = pd.read_csv("Unemployment_Rate_upto_11_2020.csv")

# Clean Columns
df.columns = df.columns.str.strip()

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# Create COVID Period Column
df["Period"] = df["Date"].apply(
    lambda x: "Before COVID" if x < pd.Timestamp("2020-03-01") else "After COVID"
)

# Average Unemployment
before_avg = round(
    df[df["Period"] == "Before COVID"]
    ["Estimated Unemployment Rate (%)"]
    .mean(),
    2
)

after_avg = round(
    df[df["Period"] == "After COVID"]
    ["Estimated Unemployment Rate (%)"]
    .mean(),
    2
)

# Metrics
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Before COVID",
        f"{before_avg}%"
    )

with col2:
    st.metric(
        "After COVID",
        f"{after_avg}%"
    )

st.divider()

# Comparison Chart
comparison_df = pd.DataFrame({
    "Period": ["Before COVID", "After COVID"],
    "Rate": [before_avg, after_avg]
})

fig = px.bar(
    comparison_df,
    x="Period",
    y="Rate",
    color="Period",
    title="Average Unemployment Rate"
)

st.plotly_chart(fig, use_container_width=True)

# Monthly Trend
st.subheader("📈 Monthly Unemployment Trend During COVID")

monthly = (
    df.groupby("Date")
    ["Estimated Unemployment Rate (%)"]
    .mean()
    .reset_index()
)

fig2 = px.line(
    monthly,
    x="Date",
    y="Estimated Unemployment Rate (%)",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# Most Affected States
st.subheader("⚠ Most Affected States")

state_data = (
    df.groupby("Region")
    ["Estimated Unemployment Rate (%)"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig3 = px.bar(
    x=state_data.values,
    y=state_data.index,
    orientation="h",
    title="Top 10 States with Highest Unemployment"
)

st.plotly_chart(fig3, use_container_width=True)

# Dataset
with st.expander("📄 View Dataset"):
    st.dataframe(df)