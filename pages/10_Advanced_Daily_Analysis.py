import streamlit as st
import plotly.express as px

from config import SESSION_DF_KEY
from utils.column_detector import auto_detect_columns
from utils.safe_dataframe import prepare_daily_sales_df

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Advanced Daily Sales Analysis",
    layout="wide"
)

st.title("📈 Advanced Daily Sales Analysis")
st.caption("Enterprise-grade daily trend, volatility & momentum view")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Please upload data or connect Snowflake first.")
    st.stop()

# -------------------------------------------------
# AUTO COLUMN DETECTION
# -------------------------------------------------
cols = auto_detect_columns(df)

date_col = cols.get("date")
sales_col = cols.get("sales")

if not date_col or not sales_col:
    st.error("❌ Date or Sales column could not be detected.")
    st.stop()

# -------------------------------------------------
# PREPARE DAILY DATA
# -------------------------------------------------
try:
    daily_df = prepare_daily_sales_df(
        df=df,
        date_col=date_col,
        sales_col=sales_col
    )
except Exception as e:
    st.error("❌ Unable to generate daily analysis")
    st.code(str(e))
    st.stop()

# -------------------------------------------------
# KPI SUMMARY
# -------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales", f"₹{daily_df['Daily_Sales'].sum():,.0f}")

with col2:
    st.metric("Avg Daily Sales", f"₹{daily_df['Daily_Sales'].mean():,.0f}")

with col3:
    st.metric("Active Days", daily_df.shape[0])

st.divider()

# -------------------------------------------------
# DAILY SALES TREND
# -------------------------------------------------
fig = px.line(
    daily_df,
    x=date_col,
    y=["Daily_Sales", "7D_Rolling_Avg", "14D_Rolling_Avg"],
    title="Daily Sales with Rolling Averages",
    labels={"value": "Sales Value", "variable": "Metric"},
)

fig.update_layout(
    hovermode="x unified",
    legend_title_text="",
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# EXECUTIVE NOTE
# -------------------------------------------------
st.success(
    """
🧠 **Executive Insight**

This view highlights short-term volatility (daily),
mid-term momentum (7-day), and trend stability (14-day).
Use this for demand planning, stock positioning, and field execution alignment.
"""
)
