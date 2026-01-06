import streamlit as st
import plotly.express as px

from utils.safe_dataframe import prepare_daily_sales_df
from utils.helpers import get_loaded_dataframe


st.set_page_config(
    page_title="Advanced Daily Analysis",
    layout="wide"
)

st.title("📈 Advanced Daily Sales Analysis")
st.caption("Daily trends, rolling performance & executive-level insights")

# ------------------------------------
# LOAD DATA
# ------------------------------------
df = get_loaded_dataframe()

if df is None or df.empty:
    st.warning("Please upload FMCG data to view analysis.")
    st.stop()

# ------------------------------------
# COLUMN DETECTION
# ------------------------------------
DATE_COL = "ORDER_DATE"
SALES_COL = "AMOUNT"

if DATE_COL not in df.columns or SALES_COL not in df.columns:
    st.error("Required columns ORDER_DATE or AMOUNT not found.")
    st.stop()

# ------------------------------------
# PREPARE DATA (SAFE)
# ------------------------------------
try:
    daily_df = prepare_daily_sales_df(
        df=df,
        date_col=DATE_COL,
        sales_col=SALES_COL
    )
except Exception as e:
    st.error("Daily aggregation failed.")
    st.exception(e)
    st.stop()

# ------------------------------------
# KPI ROW
# ------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Sales",
        f"₹{daily_df['Daily_Sales'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Avg Daily Sales",
        f"₹{daily_df['Daily_Sales'].mean():,.0f}"
    )

with col3:
    st.metric(
        "Active Days",
        f"{daily_df['Date'].nunique()}"
    )

st.divider()

# ------------------------------------
# DAILY SALES TREND
# ------------------------------------
fig = px.line(
    daily_df,
    x="Date",
    y=["Daily_Sales", "7D_Rolling_Avg", "14D_Rolling_Avg"],
    title="Daily Sales with Rolling Averages",
    labels={
        "value": "Sales Amount",
        "variable": "Metric"
    }
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------
# DATA PREVIEW
# ------------------------------------
with st.expander("📄 View Daily Aggregated Data"):
    st.dataframe(daily_df, use_container_width=True)
