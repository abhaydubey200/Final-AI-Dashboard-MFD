# pages/7_Sales_Forecasting.py
# -------------------------------------------------
# Sales Forecasting & Demand Planning
# -------------------------------------------------

import streamlit as st
import plotly.express as px

from utils.forecasting import prepare_time_series, forecast_sales
from utils.column_detector import auto_detect_columns

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Sales Forecasting & Demand Planning | DS Group",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sales Forecasting & Demand Planning")
st.caption(
    "AI-driven monthly sales forecasting for inventory planning, budgeting, "
    "and leadership decision-making."
)

st.divider()

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("📤 Upload dataset or connect Snowflake first.")
    st.stop()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

date_col = cols.get("date")
sales_col = cols.get("sales")

if not date_col or not sales_col:
    st.error("❌ Date or Sales column not detected in dataset.")
    st.stop()

# -------------------------------------------------
# Forecast Configuration
# -------------------------------------------------
st.subheader("⚙ Forecast Configuration")

c1, c2 = st.columns(2)

with c1:
    months = st.slider(
        "Forecast Horizon (Months)",
        min_value=3,
        max_value=24,
        value=12
    )

with c2:
    freq = st.selectbox(
        "Forecast Frequency",
        ["Monthly"],
        disabled=True
    )

# -------------------------------------------------
# Prepare Time Series (STANDARDIZED OUTPUT)
# -------------------------------------------------
ts_df = prepare_time_series(df, date_col, sales_col)

# ---- HARD STANDARDIZATION (CRITICAL FIX) ----
# Ensure consistent column names for ALL downstream logic
ts_df = ts_df.rename(
    columns={
        ts_df.columns[0]: "Date",
        ts_df.columns[1]: "Sales"
    }
)

# -------------------------------------------------
# Historical Sales Trend
# -------------------------------------------------
st.subheader("📊 Historical Sales Trend")

fig1 = px.line(
    ts_df,
    x="Date",
    y="Sales",
    markers=True,
    title="Historical Sales Performance"
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------------------------
# Forecast Sales
# -------------------------------------------------
st.subheader("🔮 Sales Forecast")

forecast_df = forecast_sales(ts_df, periods=months)

# ---- STANDARDIZE FORECAST OUTPUT ----
forecast_df = forecast_df.rename(
    columns={
        forecast_df.columns[0]: "Date",
        forecast_df.columns[1]: "Sales"
    }
)

fig2 = px.line(
    forecast_df,
    x="Date",
    y="Sales",
    markers=True,
    title="Forecasted Sales"
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------
# Actual vs Forecast Comparison
# -------------------------------------------------
st.subheader("📈 Actual vs Forecast Comparison")

actual_df = ts_df.copy()
actual_df["Type"] = "Actual"

forecast_plot_df = forecast_df.copy()
forecast_plot_df["Type"] = "Forecast"

final_df = actual_df._append(forecast_plot_df, ignore_index=True)

fig3 = px.line(
    final_df,
    x="Date",
    y="Sales",
    color="Type",
    markers=True,
    title="Actual vs Forecast Sales"
)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------
# Executive Insight
# -------------------------------------------------
st.info(
    "🧠 **Executive Insight:**\n\n"
    "- Supports demand planning and inventory optimization\n"
    "- Enables proactive budgeting and capacity planning\n"
    "- Improves leadership visibility into future growth trends"
)

st.success("✅ Sales Forecast generated successfully")
