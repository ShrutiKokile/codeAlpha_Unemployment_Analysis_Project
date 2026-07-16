import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏙 State Analysis")

# Load Data
df = pd.read_csv("Unemployment in India.csv")

# Clean Column Names
df.columns = df.columns.str.strip()

# Remove empty regions
df = df.dropna(subset=["Region"])

# Convert Region to string
df["Region"] = df["Region"].astype(str)

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# State List
states = sorted(df["Region"].unique())

# Dropdown
state = st.selectbox(
    "Select a State",
    states
)

# Filter Data
state_df = df[df["Region"] == state]

# Metrics
avg_rate = round(
    state_df["Estimated Unemployment Rate (%)"].mean(),
    2
)

avg_employed = int(
    state_df["Estimated Employed"].mean()
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Average Unemployment Rate",
        f"{avg_rate}%"
    )

with col2:
    st.metric(
        "Average Employment",
        f"{avg_employed:,}"
    )

st.divider()

# Trend Graph
st.subheader(f"📈 {state} Unemployment Trend")

fig = px.line(
    state_df,
    x="Date",
    y="Estimated Unemployment Rate (%)",
    markers=True,
    title=f"Unemployment Trend in {state}"
)

st.plotly_chart(fig, use_container_width=True)

# Rural vs Urban
st.subheader("🏡 Rural vs Urban Comparison")

if "Area" in state_df.columns:

    area_data = (
        state_df.groupby("Area")
        ["Estimated Unemployment Rate (%)"]
        .mean()
        .reset_index()
    )

    fig2 = px.bar(
        area_data,
        x="Area",
        y="Estimated Unemployment Rate (%)",
        color="Area",
        title="Rural vs Urban Unemployment"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Labour Participation
st.subheader("👥 Labour Participation Rate")

fig3 = px.line(
    state_df,
    x="Date",
    y="Estimated Labour Participation Rate (%)",
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

# Employment Distribution
st.subheader("💼 Employment Distribution")

fig4 = px.histogram(
    state_df,
    x="Estimated Employed",
    nbins=20
)

st.plotly_chart(fig4, use_container_width=True)

# State Dataset
with st.expander("📄 View State Data"):
    st.dataframe(state_df)