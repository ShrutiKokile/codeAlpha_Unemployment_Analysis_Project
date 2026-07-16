import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Unemployment Dashboard")

# Load Data
df = pd.read_csv("Unemployment in India.csv")

# Clean Column Names
df.columns = df.columns.str.strip()

# Convert Date
df['Date'] = pd.to_datetime(df['Date'])

# Metrics
avg_rate = round(df['Estimated Unemployment Rate (%)'].mean(), 2)

total_states = df['Region'].nunique()

st.metric("Average Unemployment Rate", f"{avg_rate}%")
st.metric("Total States/Regions", total_states)

st.divider()

# Unemployment Trend
st.subheader("📈 Unemployment Trend Over Time")

monthly = df.groupby('Date')[
    'Estimated Unemployment Rate (%)'
].mean().reset_index()

fig = px.line(
    monthly,
    x='Date',
    y='Estimated Unemployment Rate (%)',
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# Top States
st.subheader("🏆 Top 10 States with Highest Unemployment")

state_data = (
    df.groupby('Region')
    ['Estimated Unemployment Rate (%)']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig2 = px.bar(
    x=state_data.values,
    y=state_data.index,
    orientation='h',
    labels={
        'x':'Unemployment Rate (%)',
        'y':'State'
    }
)

st.plotly_chart(fig2, use_container_width=True)

# Raw Data
with st.expander("View Dataset"):
    st.dataframe(df)