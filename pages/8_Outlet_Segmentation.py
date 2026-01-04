import streamlit as st
import plotly.express as px
from utils.risk_engine import outlet_risk_score
from utils.column_detector import auto_detect_columns

st.markdown("<div class='page-title'>🏭 Outlet Risk Intelligence</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Churn & Risk Monitoring</div>", unsafe_allow_html=True)

df = st.session_state.get("df")
if df is None:
    st.warning("Upload data or connect Snowflake")
    st.stop()

cols = auto_detect_columns(df)

outlet_col = cols.get("outlet")
date_col = cols.get("date")
sales_col = cols.get("sales")

if not outlet_col or not date_col or not sales_col:
    st.error("Required columns not detected")
    st.stop()

risk_df = outlet_risk_score(df, outlet_col, date_col, sales_col)

# ----------------------------
# KPI SNAPSHOT
# ----------------------------
c1, c2, c3 = st.columns(3)

c1.metric("High Risk Outlets", (risk_df["Risk_Level"] == "High").sum())
c2.metric("Medium Risk Outlets", (risk_df["Risk_Level"] == "Medium").sum())
c3.metric("Low Risk Outlets", (risk_df["Risk_Level"] == "Low").sum())

st.divider()

# ----------------------------
# RISK DISTRIBUTION
# ----------------------------
fig = px.bar(
    risk_df,
    x="Risk_Level",
    title="Outlet Risk Distribution",
    color="Risk_Level",
    color_discrete_map={
        "High": "red",
        "Medium": "orange",
        "Low": "green"
    }
)
st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# RISK TABLE
# ----------------------------
st.subheader("📋 Outlet Risk Details")
st.dataframe(risk_df, use_container_width=True)
