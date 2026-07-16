import streamlit as st
import pandas as pd

st.title("💡 Policy Recommendation Engine")

# Load Data
df = pd.read_csv("Unemployment in India.csv")

df.columns = df.columns.str.strip()

# Remove empty regions
df = df.dropna(subset=["Region"])

# State Selection
state = st.selectbox(
    "Select State",
    sorted(df["Region"].astype(str).unique())
)

# State Data
state_df = df[df["Region"] == state]

avg_rate = round(
    state_df["Estimated Unemployment Rate (%)"].mean(),
    2
)

# Employment Health Score
health_score = round(
    100 - avg_rate,
    2
)

st.metric(
    "Average Unemployment Rate",
    f"{avg_rate}%"
)

st.metric(
    "Employment Health Score",
    health_score
)

# Risk Category
if avg_rate >= 20:

    st.error("🔴 High Risk State")

    st.write("""
    Recommended Policies:

    • Launch Skill Development Programs

    • Increase MSME Support

    • Create Government Employment Schemes

    • Encourage Startup Ecosystem

    • Improve Industrial Investments
    """)

elif avg_rate >= 10:

    st.warning("🟡 Medium Risk State")

    st.write("""
    Recommended Policies:

    • Expand Vocational Training

    • Improve Job Matching Platforms

    • Support Small Businesses

    • Increase Private Sector Hiring
    """)

else:

    st.success("🟢 Low Risk State")

    st.write("""
    Recommended Policies:

    • Maintain Current Policies

    • Focus on Innovation

    • Encourage High-Skill Employment

    • Promote Entrepreneurship
    """)

st.divider()

st.subheader("Project Conclusion")

st.write("""
This recommendation system uses unemployment rates to
identify risk levels and suggest employment policies
for different states.
""")