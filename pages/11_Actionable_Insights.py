import streamlit as st
import pandas as pd
import numpy as np

from config import SESSION_DF_KEY, HIGH_CHURN_DAYS
from utils.column_detector import auto_detect_columns
from utils.churn_analysis import churn_risk

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Actionable Business Insights",
    layout="wide"
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Upload dataset or connect Snowflake first.")
    st.stop()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("🧠 Actionable Business Insights")
st.markdown(
    "Auto-generated **business risks, opportunities, and recommendations** for leadership."
)

st.divider()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

date_col = cols.get("date")
sales_col = cols.get("sales")
sku_col = cols.get("sku")
outlet_col = cols.get("outlet")

if not date_col or not sales_col:
    st.error("❌ Required Date/Sales columns not detected.")
    st.stop()

# -------------------------------------------------
# Time-Based Sales Trend
# -------------------------------------------------
df[date_col] = pd.to_datetime(df[date_col])

monthly_sales = (
    df
    .groupby(pd.Grouper(key=date_col, freq="M"))
    .agg(Monthly_Sales=(sales_col, "sum"))
    .reset_index()
    .sort_values(date_col)
)

monthly_sales["Growth_%"] = monthly_sales["Monthly_Sales"].pct_change() * 100

# -------------------------------------------------
# Insight Containers
# -------------------------------------------------
risk_insights = []
opportunity_insights = []
action_items = []

# -------------------------------------------------
# Sales Decline Risk
# -------------------------------------------------
if len(monthly_sales) >= 3:
    recent_growth = monthly_sales["Growth_%"].iloc[-1]

    if recent_growth < -5:
        risk_insights.append(
            "📉 **Sales Decline Detected**: Recent month shows a significant drop (>5%)."
        )
        action_items.append(
            "Investigate pricing, distributor coverage, and stock availability immediately."
        )

# -------------------------------------------------
# SKU Concentration Risk
# -------------------------------------------------
if sku_col:
    sku_sales = (
        df
        .groupby(sku_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
    )

    top_sku_share = sku_sales.iloc[0] / sku_sales.sum() * 100

    if top_sku_share > 40:
        risk_insights.append(
            f"⚠️ **High SKU Dependency**: Top SKU contributes {top_sku_share:.1f}% of sales."
        )
        action_items.append(
            "Reduce dependency by promoting secondary SKUs and bundling."
        )

# -------------------------------------------------
# Outlet Churn Risk
# -------------------------------------------------
if outlet_col and date_col:
    churn_df = churn_risk(df, outlet_col, date_col)
    high_risk_count = (churn_df["Churn_Risk"] == "High").sum()

    if high_risk_count > 0:
        risk_insights.append(
            f"🚨 **Outlet Churn Risk**: {high_risk_count} outlets inactive for > {HIGH_CHURN_DAYS} days."
        )
        action_items.append(
            "Launch reactivation offers and route re-planning for inactive outlets."
        )

# -------------------------------------------------
# Opportunity Detection
# -------------------------------------------------
if "Growth_%" in monthly_sales.columns:
    if monthly_sales["Growth_%"].mean() > 3:
        opportunity_insights.append(
            "🚀 **Consistent Growth**: Average monthly growth above 3%."
        )
        action_items.append(
            "Increase production & distributor allocation to capture momentum."
        )

# -------------------------------------------------
# Display Insights
# -------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🚨 Risks")
    if risk_insights:
        for r in risk_insights:
            st.markdown(f"- {r}")
    else:
        st.success("No critical risks detected.")

with col2:
    st.subheader("🌱 Opportunities")
    if opportunity_insights:
        for o in opportunity_insights:
            st.markdown(f"- {o}")
    else:
        st.info("No major opportunities identified.")

with col3:
    st.subheader("📌 Recommended Actions")
    if action_items:
        for a in action_items:
            st.markdown(f"- {a}")
    else:
        st.success("Continue current strategy.")

# -------------------------------------------------
# Executive Summary
# -------------------------------------------------
st.divider()
st.success(
    """
🧾 **Executive Summary**

This intelligence layer converts raw analytics into **decision-ready insights**.
Designed for leadership reviews, board decks, and quarterly planning.
"""
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Actionable Insights Engine • DS Group FMCG Analytics Platform")
