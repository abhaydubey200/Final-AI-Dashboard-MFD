# pages/7_Sales_Forecasting.py
# --------------------------------------------------
# 📈 Sales Forecasting & Demand Planning (PRODUCTION)
# --------------------------------------------------

import streamlit as st
import pandas as pd

from utils.column_detector import auto_detect_columns
from utils.forecasting import forecast_sales

st.header("📈 Sales Forecasting & Demand Planning")
st.caption(
    "AI-driven monthly sales forecasting for inventory planning, budgeting, and leadership decision-making."
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("Please upload a dataset first.")
    st.stop()

# --------------------------------------------------
# Auto Detect Columns (CRITICAL)
# --------------------------------------------------
cols = auto_detect_columns(df)

date_col = cols.get("date")
sales_col = cols.get("sales")

if not date_col or not sales_col:
    st.error("Date or Sales column could not be detected.")
    st.stop()

# --------------------------------------------------
# Data Preparation (PROPHET SAFE)
# --------------------------------------------------
data = df[[date_col, sales_col]].copy()
data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
data = data.dropna()

if data.empty:
    st.error("No valid date/sales data available.")
    st.stop()

# Monthly aggregation (MANDATORY)
data["Month"] = data[date_col].dt.to_period("M").dt.to_timestamp()

monthly = (
    data.groupby("Month", as_index=False)[sales_col]
    .sum()
    .rename(columns={"Month": "ds", sales_col: "y"})
)

if len(monthly) < 6:
    st.warning("At least 6 months of data required for forecasting.")
    st.stop()

# --------------------------------------------------
# Forecast Controls
# --------------------------------------------------
st.subheader("⚙ Forecast Configuration")

months = st.slider(
    "Forecast Horizon (Months)",
    min_value=3,
    max_value=24,
    value=12
)

# --------------------------------------------------
# Run Forecast (UTILS)
# --------------------------------------------------
try:
    forecast_df = forecast_sales(monthly, periods=months)
except Exception as e:
    st.error("Forecasting failed. Check data quality.")
    st.exception(e)
    st.stop()

# --------------------------------------------------
# KPIs
# --------------------------------------------------
st.subheader("📊 Forecast KPIs")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Forecast Sales",
    f"₹ {forecast_df['yhat'].tail(months).sum():,.0f}"
)

c2.metric(
    "Avg Monthly Forecast",
    f"₹ {forecast_df['yhat'].tail(months).mean():,.0f}"
)

c3.metric(
    "Peak Forecast Month",
    forecast_df.loc[forecast_df["yhat"].idxmax(), "ds"].strftime("%b %Y")
)

# --------------------------------------------------
# Visualization
# --------------------------------------------------
st.subheader("📉 Actual vs Forecast")

plot_df = pd.concat(
    [
        monthly.assign(Type="Actual"),
        forecast_df[["ds", "yhat"]]
        .rename(columns={"yhat": "y"})
        .assign(Type="Forecast"),
    ],
    ignore_index=True,
)

st.line_chart(
    plot_df.set_index("ds")["y"],
    use_container_width=True
)

# --------------------------------------------------
# Forecast Table
# --------------------------------------------------
st.subheader("📋 Forecast Table")

table = forecast_df.tail(months)[["ds", "yhat"]].copy()
table["Month"] = table["ds"].dt.strftime("%b %Y")
table["Predicted Sales"] = table["yhat"].round(0)

st.dataframe(
    table[["Month", "Predicted Sales"]],
    use_container_width=True
)

# --------------------------------------------------
# Success
# --------------------------------------------------
st.success("Sales Forecast generated successfully ✅")
