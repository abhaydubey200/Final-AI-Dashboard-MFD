# pages/7_Sales_Forecasting.py
# -------------------------------------------------
# Sales Forecasting (Time-Series)
# -------------------------------------------------

import streamlit as st
import plotly.express as px

from utils.column_detector import auto_detect_columns
from utils.forecasting import prepare_time_series, forecast_sales

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Sales Forecasting | DS Group",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Sales Forecasting")
st.caption(
    "Predict future sales trends to support "
    "**inventory planning, budgeting, and growth strategy**"
)

st.divider()

# -------------------------------------------------
# Load Dataset (Upload / Snowflake)
# -------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("📤 Upload dataset or connect Snowflake to continue.")
    st.stop()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

date_col = cols.get("date")
sales_col = cols.get("sales")

# -------------------------------------------------
# Validation
# -------------------------------------------------
if not date_col or not sales_col:
    st.error(
        "❌ Required columns not detected.\n\n"
        f"- Date column: `{date_col}`\n"
        f"- Sales column: `{sales_col}`"
    )
    st.stop()

# -------------------------------------------------
# Prepare Time Series
# -------------------------------------------------
try:
    ts_df = prepare_time_series(df, date_col, sales_col)
except Exception as e:
    st.error("❌ Failed to prepare time-series data.")
    st.exception(e)
    st.stop()

# -------------------------------------------------
# Historical Sales Trend
# -------------------------------------------------
st.subheader("📊 Historical Sales Trend")

fig_hist = px.line(
    ts_df,
    x="Date",
    y="Sales",
    markers=True,
    title="Historical Sales Performance"
)

fig_hist.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales",
    template="plotly_white"
)

st.plotly_chart(fig_hist, use_container_width=True)

# -------------------------------------------------
# Forecast Controls
# -------------------------------------------------
st.subheader("🔮 Forecast Settings")

forecast_months = st.slider(
    "Forecast Duration (Months)",
    min_value=3,
    max_value=24,
    value=12,
    help="Select how many months into the future to forecast"
)

# -------------------------------------------------
# Forecast Generation
# -------------------------------------------------
try:
    forecast_df = forecast_sales(ts_df, periods=forecast_months)
except Exception as e:
    st.error("❌ Forecasting failed. Please check data quality.")
    st.exception(e)
    st.stop()

# -------------------------------------------------
# Forecast Plot
# -------------------------------------------------
st.subheader("📈 Forecasted Sales")

fig_forecast = px.line(
    forecast_df,
    x="Date",
    y="Sales",
    markers=True,
    title="Forecasted Sales Trend"
)

fig_forecast.update_layout(
    xaxis_title="Date",
    yaxis_title="Forecasted Sales",
    template="plotly_white"
)

st.plotly_chart(fig_forecast, use_container_width=True)

# -------------------------------------------------
# Actual vs Forecast Comparison
# -------------------------------------------------
st.subheader("📊 Actual vs Forecast Comparison")

actual_df = ts_df.copy()
actual_df["Type"] = "Actual"

forecast_plot_df = forecast_df.copy()
forecast_plot_df["Type"] = "Forecast"

comparison_df = actual_df._append(
    forecast_plot_df,
    ignore_index=True
)

fig_compare = px.line(
    comparison_df,
    x="Date",
    y="Sales",
    color="Type",
    markers=True,
    title="Actual vs Forecast Sales"
)

fig_compare.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales",
    template="plotly_white"
)

st.plotly_chart(fig_compare, use_container_width=True)

# -------------------------------------------------
# Business Insights
# -------------------------------------------------
st.info(
    "📌 **How to use this forecast:**\n\n"
    "- 📦 Plan inventory and warehouse capacity\n"
    "- 💰 Improve budget and cash-flow forecasting\n"
    "- 🏭 Align production with future demand\n"
    "- 🎯 Support strategic sales targets"
)

st.success("✅ Sales forecast generated successfully")
