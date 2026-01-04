import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from config import (
    SESSION_DF_KEY,
    DEFAULT_FORECAST_MONTHS,
    MAX_FORECAST_MONTHS,
    ENABLE_PROPHET
)

from utils.column_detector import auto_detect_columns
from utils.forecasting import prepare_time_series, forecast_sales

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Sales Forecasting",
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
# Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)
date_col = cols.get("date")
sales_col = cols.get("sales")

if not date_col or not sales_col:
    st.error("❌ Date or Sales column could not be detected.")
    st.stop()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("📈 Sales Forecasting & Demand Planning")
st.markdown(
    "AI-driven **monthly sales forecasting** for inventory planning, "
    "budgeting, and leadership decision-making."
)

st.divider()

# -------------------------------------------------
# Filters
# -------------------------------------------------
with st.expander("⚙ Forecast Configuration", expanded=True):

    c1, c2 = st.columns(2)

    with c1:
        horizon = st.slider(
            "Forecast Horizon (Months)",
            min_value=3,
            max_value=MAX_FORECAST_MONTHS,
            value=DEFAULT_FORECAST_MONTHS
        )

    with c2:
        freq = st.selectbox(
            "Forecast Frequency",
            options=["M"],
            format_func=lambda x: "Monthly"
        )

# -------------------------------------------------
# Prepare Time Series
# -------------------------------------------------
ts_df = prepare_time_series(
    df,
    date_col=date_col,
    sales_col=sales_col,
    freq=freq
)

if ts_df.empty or len(ts_df) < 6:
    st.error("❌ Not enough historical data for forecasting.")
    st.stop()

# -------------------------------------------------
# Forecast
# -------------------------------------------------
forecast_df = forecast_sales(
    ts_df,
    periods=horizon
)

# -------------------------------------------------
# Combine Actual + Forecast
# -------------------------------------------------
actual_df = ts_df[["Date", "Sales"]].copy()
actual_df["Type"] = "Actual"

forecast_df["Type"] = "Forecast"

plot_df = pd.concat(
    [actual_df, forecast_df],
    ignore_index=True
)

# -------------------------------------------------
# KPIs
# -------------------------------------------------
st.markdown("## 📌 Forecast KPIs")

k1, k2, k3 = st.columns(3)

k1.metric(
    "📅 Forecast Period",
    f"{horizon} Months"
)

k2.metric(
    "💰 Total Forecast Sales",
    f"{forecast_df['Sales'].sum():,.0f}"
)

k3.metric(
    "📊 Avg Monthly Sales",
    f"{forecast_df['Sales'].mean():,.0f}"
)

st.divider()

# -------------------------------------------------
# Forecast Chart
# -------------------------------------------------
st.markdown("## 📉 Actual vs Forecast Trend")

fig = px.line(
    plot_df,
    x="Date",
    y="Sales",
    color="Type",
    markers=True,
    title="Sales Forecast (Monthly)"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Forecast Table
# -------------------------------------------------
st.markdown("## 📋 Forecast Output")

table_df = forecast_df.copy()
table_df["Month"] = table_df["Date"].dt.strftime("%b %Y")
table_df["Forecast_Sales"] = table_df["Sales"].round(0)

st.dataframe(
    table_df[["Month", "Forecast_Sales"]],
    use_container_width=True
)

# -------------------------------------------------
# Download
# -------------------------------------------------
csv = table_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Forecast (CSV)",
    data=csv,
    file_name="sales_forecast.csv",
    mime="text/csv"
)

# -------------------------------------------------
# Executive Insight
# -------------------------------------------------
st.success(
    """
✅ Forecast ready for:
• Inventory & production planning  
• Budget allocation  
• Growth scenario simulation  

Model used: **Random Forest (stable & explainable)**
"""
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Sales Forecasting Engine • DS Group FMCG Intelligence Platform")
