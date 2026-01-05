# pages/7_Sales_Forecasting.py
# --------------------------------------------------
# 📈 Sales Forecasting & Demand Planning (PRODUCTION)
# --------------------------------------------------

import streamlit as st
import pandas as pd

from utils.column_detector import auto_detect_columns
from utils.data_processing import preprocess
from utils.forecasting import prepare_time_series, forecast_sales
from utils.visualizations import line_sales_trend

st.header("📈 Sales Forecasting & Demand Planning")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("Please upload a dataset first.")
    st.stop()

# --------------------------------------------------
# Detect Columns
# --------------------------------------------------
cols = auto_detect_columns(df)

date_col = cols.get("date")
sales_col = cols.get("sales")

if not date_col or not sales_col:
    st.error("Required columns missing: Date or Sales")
    st.stop()

# --------------------------------------------------
# Preprocess
# --------------------------------------------------
df = preprocess(df, date_col)

if df.empty:
    st.warning("No valid data available after preprocessing.")
    st.stop()

# --------------------------------------------------
# Forecast Configuration
# --------------------------------------------------
st.subheader("⚙ Forecast Configuration")

col1, col2 = st.columns(2)

with col1:
    months = st.slider(
        "Forecast Horizon (Months)",
        min_value=3,
        max_value=24,
        value=6
    )

with col2:
    freq = st.selectbox(
        "Forecast Frequency",
        options=["Monthly"],
        index=0
    )

# --------------------------------------------------
# Prepare Time Series
# --------------------------------------------------
try:
    ts_df = prepare_time_series(
        df=df,
        date_col=date_col,
        sales_col=sales_col,
        freq="M"
    )
except Exception as e:
    st.error(f"Failed to prepare time series: {e}")
    st.stop()

if ts_df is None or ts_df.empty or len(ts_df) < 2:
    st.warning("Not enough historical data for forecasting.")
    st.stop()

# --------------------------------------------------
# Actual Sales Chart
# --------------------------------------------------
st.subheader("📊 Historical Sales Trend")

try:
    st.plotly_chart(
        line_sales_trend(ts_df, "Date", "Sales"),
        use_container_width=True
    )
except Exception:
    st.info("Unable to render historical chart.")

# --------------------------------------------------
# Forecast
# --------------------------------------------------
st.subheader("🔮 Sales Forecast")

try:
    forecast_df = forecast_sales(ts_df, periods=months)
except Exception as e:
    st.error(f"Forecasting failed: {e}")
    st.stop()

if forecast_df is None or forecast_df.empty:
    st.warning("Forecast could not be generated.")
    st.stop()

# --------------------------------------------------
# Combine Actual + Forecast
# --------------------------------------------------
actual_df = ts_df.copy()
actual_df["Type"] = "Actual"

forecast_df = forecast_df.copy()
forecast_df["Type"] = "Forecast"

combined_df = pd.concat(
    [actual_df, forecast_df],
    ignore_index=True
)

# --------------------------------------------------
# Forecast Visualization
# --------------------------------------------------
try:
    st.plotly_chart(
        line_sales_trend(
            combined_df,
            date_col="Date",
            sales_col="Sales"
        ),
        use_container_width=True
    )
except Exception:
    st.info("Forecast chart could not be rendered.")

# --------------------------------------------------
# Forecast Table
# --------------------------------------------------
st.subheader("📄 Forecast Data")

st.dataframe(
    forecast_df.style.format({"Sales": "{:,.0f}"}),
    use_container_width=True
)

# --------------------------------------------------
# Summary
# --------------------------------------------------
st.success("Forecast generated successfully ✅")
