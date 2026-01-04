import streamlit as st
from utils.kpi_engine import generate_kpis
from utils.ai_summary import generate_ceo_summary

st.markdown("<div class='page-title'>📊 Executive Overview</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>CEO & Board Summary</div>", unsafe_allow_html=True)

df = st.session_state.get("df")

if df is None:
    st.warning("Please upload data or connect Snowflake")
    st.stop()

# -------------------------------
# CONFIG (later auto-detected)
# -------------------------------
DATE_COL = "date"
SALES_COL = "sales"

# -------------------------------
# KPI ENGINE
# -------------------------------
kpis = generate_kpis(df, DATE_COL, SALES_COL)

# -------------------------------
# KPI CARDS
# -------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Current Month Sales", f"₹{kpis['Current Month Sales']:,.0f}")
c2.metric("Previous Month Sales", f"₹{kpis['Previous Month Sales']:,.0f}")
c3.metric("MoM Growth", f"{kpis['MoM Growth %']}%")
c4.metric("YTD Sales", f"₹{kpis['YTD Sales']:,.0f}")

st.divider()

# -------------------------------
# AI CEO SUMMARY
# -------------------------------
st.markdown("## 🧠 AI Executive Summary")

summary = generate_ceo_summary(kpis)
st.markdown(summary)
