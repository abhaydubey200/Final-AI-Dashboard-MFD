import streamlit as st
import pandas as pd
import plotly.express as px

from config import SESSION_DF_KEY, CURRENCY_SYMBOL
from utils.column_detector import auto_detect_columns

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Daily Sales Analysis",
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
st.title("📅 Daily Sales Analysis")
st.markdown(
    "Granular **day-level revenue intelligence** with growth trend indicators."
)

st.divider()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

date_col = cols.get("date")
sales_col = cols.get("sales")

if not date_col or not sales_col:
    st.error("❌ Date or Sales column not detected.")
    st.stop()

# -------------------------------------------------
# Prepare Daily Aggregation
# -------------------------------------------------
daily_df = df.copy()
daily_df[date_col] = pd.to_datetime(daily_df[date_col])

daily_df = (
    daily_df
    .groupby(pd.Grouper(key=date_col, freq="D"))
    .agg(Daily_Sales=(sales_col, "sum"))
    .reset_index()
    .rename(columns={date_col: "Date"})
)

daily_df.sort_values("Date", inplace=True)

# -------------------------------------------------
# Growth Calculations
# -------------------------------------------------
daily_df["MoM_Growth_%"] = daily_df["Daily_Sales"].pct_change(30) * 100
daily_df["YoY_Growth_%"] = daily_df["Daily_Sales"].pct_change(365) * 100

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------
st.markdown("## 📌 Key Daily KPIs")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Total Sales",
    f"{CURRENCY_SYMBOL}{daily_df['Daily_Sales'].sum():,.0f}"
)

k2.metric(
    "Avg Daily Sales",
    f"{CURRENCY_SYMBOL}{daily_df['Daily_Sales'].mean():,.0f}"
)

latest_mom = daily_df["MoM_Growth_%"].iloc[-1]
latest_yoy = daily_df["YoY_Growth_%"].iloc[-1]

k3.metric(
    "MoM Growth",
    f"{latest_mom:.2f}%",
    delta=f"{latest_mom:.2f}%"
)

k4.metric(
    "YoY Growth",
    f"{latest_yoy:.2f}%",
    delta=f"{latest_yoy:.2f}%"
)

st.divider()

# -------------------------------------------------
# Daily Sales Trend
# -------------------------------------------------
st.markdown("## 📈 Daily Sales Trend")

fig1 = px.line(
    daily_df,
    x="Date",
    y="Daily_Sales",
    markers=True,
    title="Daily Sales Performance"
)

fig1.update_layout(template="plotly_white")

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------------------------
# Growth Trend Visualization
# -------------------------------------------------
st.markdown("## 📊 Growth Trend Analysis")

growth_df = daily_df.dropna(subset=["MoM_Growth_%", "YoY_Growth_%"])

fig2 = px.line(
    growth_df,
    x="Date",
    y=["MoM_Growth_%", "YoY_Growth_%"],
    title="MoM vs YoY Growth Trend"
)

fig2.update_layout(template="plotly_white")

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------
# Daily Sales Table
# -------------------------------------------------
st.markdown("## 📋 Daily Sales Table")

st.dataframe(
    daily_df.sort_values("Date", ascending=False),
    use_container_width=True
)

# -------------------------------------------------
# Executive Insight
# -------------------------------------------------
st.success(
    """
🧠 **Executive Insight**

• Sustained positive MoM indicates healthy **distribution momentum**  
• Volatility in YoY suggests **seasonality or demand shifts**  
• Use this page for **early warning signals** before monthly closures
"""
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Daily Sales Intelligence • DS Group FMCG Analytics Platform")
