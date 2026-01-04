import streamlit as st
import pandas as pd
import numpy as np

from config import (
    APP_TITLE,
    SESSION_DF_KEY,
    CURRENCY_SYMBOL,
)
from utils.kpis import kpi_total_sales, kpi_orders, kpi_aov
from utils.churn_analysis import churn_risk
from utils.column_detector import auto_detect_columns

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Executive Overview | FMCG Intelligence",
    layout="wide",
)

# -------------------------------------------------
# Global CSS (MNC Style)
# -------------------------------------------------
st.markdown("""
<style>
.exec-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 10px 32px rgba(0,0,0,0.08);
    border-top: 6px solid #0aad0a;
}
.exec-title {
    font-size: 14px;
    color: #6b7280;
    font-weight: 700;
}
.exec-value {
    font-size: 30px;
    font-weight: 900;
    color: #111827;
}
.exec-sub {
    font-size: 13px;
    color: #374151;
    margin-top: 6px;
}
.section {
    background: #ffffff;
    padding: 26px;
    border-radius: 18px;
    box-shadow: 0 12px 36px rgba(0,0,0,0.07);
    margin-bottom: 28px;
}
.ai-box {
    background: linear-gradient(135deg, #ecfeff, #f0fdf4);
    border-left: 6px solid #22c55e;
    padding: 24px;
    border-radius: 18px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Please upload data or connect Snowflake first.")
    st.stop()

cols = auto_detect_columns(df)

date_col = cols.get("date")
sales_col = cols.get("sales")
outlet_col = cols.get("outlet")

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("📊 Executive Overview")
st.markdown(
    "C-level snapshot of **sales performance, growth, and business risk** across the FMCG ecosystem."
)

# -------------------------------------------------
# KPI CALCULATIONS
# -------------------------------------------------
total_sales = kpi_total_sales(df, sales_col)
orders = kpi_orders(df)
aov = kpi_aov(df, sales_col)

# Date logic for growth
df[date_col] = pd.to_datetime(df[date_col])
df["Month"] = df[date_col].dt.to_period("M")

monthly_sales = df.groupby("Month")[sales_col].sum().sort_index()

mom_growth = (
    (monthly_sales.iloc[-1] - monthly_sales.iloc[-2]) / monthly_sales.iloc[-2] * 100
    if len(monthly_sales) > 1 else 0
)

yoy_growth = (
    (monthly_sales.iloc[-1] - monthly_sales.iloc[-13]) / monthly_sales.iloc[-13] * 100
    if len(monthly_sales) > 13 else 0
)

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

def kpi(card_title, value, sub=""):
    st.markdown(f"""
    <div class="exec-card">
        <div class="exec-title">{card_title}</div>
        <div class="exec-value">{value}</div>
        <div class="exec-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

with c1:
    kpi("Total Sales", f"{CURRENCY_SYMBOL}{total_sales:,.0f}")

with c2:
    kpi("Total Orders", f"{orders:,}")

with c3:
    kpi("Avg Order Value", f"{CURRENCY_SYMBOL}{aov:,.0f}")

with c4:
    kpi("MoM Growth", f"{mom_growth:.2f}%", "Month-over-Month")

with c5:
    kpi("YoY Growth", f"{yoy_growth:.2f}%", "Year-over-Year")

st.divider()

# -------------------------------------------------
# BUSINESS RISK SNAPSHOT
# -------------------------------------------------
st.markdown("## 🏭 Business Risk Snapshot")

risk_df = churn_risk(df, outlet_col, date_col)

risk_summary = (
    risk_df["Churn_Risk"]
    .value_counts()
    .reindex(["High", "Medium", "Low"])
    .fillna(0)
)

r1, r2, r3 = st.columns(3)

with r1:
    kpi("High Risk Outlets", int(risk_summary["High"]), "Immediate action required")

with r2:
    kpi("Medium Risk Outlets", int(risk_summary["Medium"]), "Monitor closely")

with r3:
    kpi("Low Risk Outlets", int(risk_summary["Low"]), "Healthy network")

# -------------------------------------------------
# AI CEO EXECUTIVE SUMMARY
# -------------------------------------------------
st.markdown("## 🧠 AI Executive Summary (CEO View)")

summary_text = f"""
• The business generated **{CURRENCY_SYMBOL}{total_sales:,.0f}** in total sales across **{orders:,} orders**.  
• Average order value stands at **{CURRENCY_SYMBOL}{aov:,.0f}**, indicating current pricing strength.  
• Month-over-Month growth is **{mom_growth:.2f}%**, while Year-over-Year growth is **{yoy_growth:.2f}%**.  
• **{int(risk_summary['High'])} outlets** are at high churn risk and need immediate intervention.  
• Overall network health is **stable**, with majority outlets performing within acceptable thresholds.
"""

st.markdown(f"""
<div class="ai-box">
<h4>📌 Strategic Insights</h4>
<p>{summary_text}</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption(
    "Executive Intelligence powered by DS Group • Confidential • Board-Level View"
)
