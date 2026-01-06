import streamlit as st
import pandas as pd
import plotly.express as px

from config import SESSION_DF_KEY, CURRENCY_SYMBOL
from utils.column_detector import auto_detect_columns
from utils.safe_dataframe import prepare_daily_sales_df

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Advanced Daily Sales Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================================================
# LOAD DATA
# =================================================
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Please upload data or connect Snowflake to continue.")
    st.stop()

# =================================================
# HEADER
# =================================================
st.title("📈 Advanced Daily Sales Analysis")
st.caption(
    "Granular daily performance tracking with rolling averages and volatility signals"
)
st.divider()

# =================================================
# AUTO COLUMN DETECTION
# =================================================
cols = auto_detect_columns(df)

date_col = cols.get("date")
sales_col = cols.get("sales")

if not date_col or not sales_col:
    st.error("❌ Required Date or Sales column not detected.")
    st.stop()

# =================================================
# DATA PREPARATION (ENTERPRISE SAFE)
# =================================================
daily_df = prepare_daily_sales_df(
    df=df,
    date_col=date_col,
    sales_col=sales_col
)

if daily_df.empty:
    st.error("❌ No valid daily sales data after normalization.")
    st.stop()

# =================================================
# KPI ROW
# =================================================
col1, col2, col3, col4 = st.columns(4)

total_sales = daily_df["Daily_Sales"].sum()
avg_daily_sales = daily_df["Daily_Sales"].mean()
max_sales = daily_df["Daily_Sales"].max()
min_sales = daily_df["Daily_Sales"].min()

col1.metric("Total Sales", f"{CURRENCY_SYMBOL}{total_sales:,.0f}")
col2.metric("Avg Daily Sales", f"{CURRENCY_SYMBOL}{avg_daily_sales:,.0f}")
col3.metric("Highest Day", f"{CURRENCY_SYMBOL}{max_sales:,.0f}")
col4.metric("Lowest Day", f"{CURRENCY_SYMBOL}{min_sales:,.0f}")

st.divider()

# =================================================
# DAILY SALES TREND
# =================================================
st.subheader("📊 Daily Sales Trend with Rolling Averages")

fig = px.line(
    daily_df,
    x=date_col,
    y=["Daily_Sales", "7D_Rolling_Avg", "14D_Rolling_Avg"],
    labels={
        "value": "Sales Amount",
        "variable": "Metric",
        date_col: "Date"
    },
    title="Daily Sales with 7 & 14 Day Rolling Averages",
)

fig.update_layout(
    hovermode="x unified",
    legend_title_text="Metrics",
    height=500
)

st.plotly_chart(fig, width="stretch")

# =================================================
# VOLATILITY & BUSINESS SIGNALS
# =================================================
st.subheader("⚠️ Volatility & Business Signals")

daily_df["Daily_Change_%"] = daily_df["Daily_Sales"].pct_change() * 100

high_volatility_days = daily_df[
    daily_df["Daily_Change_%"].abs() > 25
]

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📉 High Volatility Days**")
    if high_volatility_days.empty:
        st.success("No abnormal volatility detected.")
    else:
        st.dataframe(
            high_volatility_days[
                [date_col, "Daily_Sales", "Daily_Change_%"]
            ].rename(columns={
                "Daily_Sales": "Sales",
                "Daily_Change_%": "Change %"
            }),
            width="stretch"
        )

with col2:
    st.markdown("**🧠 Executive Interpretation**")
    if not high_volatility_days.empty:
        st.warning(
            "Significant daily fluctuations detected. "
            "Possible drivers include promotions, stock-outs, "
            "route changes, or distributor behavior."
        )
    else:
        st.success(
            "Sales movement appears stable with no extreme deviations."
        )

st.divider()

# =================================================
# BUSINESS SUMMARY
# =================================================
st.success(
    """
### 🧾 Executive Summary

This analysis provides **day-level sales visibility** with trend smoothing
to identify **underlying performance patterns** while filtering short-term noise.

**Recommended Usage:**
- Daily leadership review  
- Route & beat performance validation  
- Promotion effectiveness tracking  
- Supply disruption detection  
"""
)

st.caption("Advanced Daily Analysis • DS Group FMCG Intelligence Platform")
