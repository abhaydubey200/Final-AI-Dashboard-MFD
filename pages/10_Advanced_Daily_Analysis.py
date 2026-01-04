import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from config import SESSION_DF_KEY, CURRENCY_SYMBOL
from utils.column_detector import auto_detect_columns

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Advanced Daily Analysis",
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
st.title("📊 Advanced Daily Sales Intelligence")
st.markdown(
    "Deep **trend, seasonality, and anomaly analysis** for executive decision-making."
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
# Daily Aggregation
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
# Rolling Averages
# -------------------------------------------------
daily_df["MA_7"] = daily_df["Daily_Sales"].rolling(7).mean()
daily_df["MA_14"] = daily_df["Daily_Sales"].rolling(14).mean()
daily_df["MA_30"] = daily_df["Daily_Sales"].rolling(30).mean()

# -------------------------------------------------
# Rolling Trend Chart
# -------------------------------------------------
st.markdown("## 📈 Rolling Sales Trend")

fig1 = px.line(
    daily_df,
    x="Date",
    y=["Daily_Sales", "MA_7", "MA_14", "MA_30"],
    title="Daily Sales with Rolling Averages"
)

fig1.update_layout(template="plotly_white")
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# -------------------------------------------------
# Seasonality Analysis (Day of Week)
# -------------------------------------------------
daily_df["Day_Name"] = daily_df["Date"].dt.day_name()

dow_df = (
    daily_df
    .groupby("Day_Name", as_index=False)
    .agg(Avg_Sales=("Daily_Sales", "mean"))
)

dow_df["Day_Name"] = pd.Categorical(
    dow_df["Day_Name"],
    categories=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    ordered=True
)

dow_df.sort_values("Day_Name", inplace=True)

st.markdown("## 🗓️ Day-of-Week Seasonality")

fig2 = px.bar(
    dow_df,
    x="Day_Name",
    y="Avg_Sales",
    title="Average Sales by Day of Week"
)

fig2.update_layout(template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# -------------------------------------------------
# Peak & Low Demand Detection
# -------------------------------------------------
st.markdown("## 🚦 Peak & Low Demand Signals")

high_threshold = daily_df["Daily_Sales"].quantile(0.90)
low_threshold = daily_df["Daily_Sales"].quantile(0.10)

daily_df["Demand_Flag"] = np.where(
    daily_df["Daily_Sales"] >= high_threshold, "Peak",
    np.where(daily_df["Daily_Sales"] <= low_threshold, "Low", "Normal")
)

fig3 = px.scatter(
    daily_df,
    x="Date",
    y="Daily_Sales",
    color="Demand_Flag",
    title="Peak & Low Demand Detection"
)

fig3.update_layout(template="plotly_white")
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# -------------------------------------------------
# Anomaly Detection (Simple Statistical)
# -------------------------------------------------
st.markdown("## 🚨 Sales Anomaly Detection")

mean_sales = daily_df["Daily_Sales"].mean()
std_sales = daily_df["Daily_Sales"].std()

daily_df["Anomaly"] = np.where(
    abs(daily_df["Daily_Sales"] - mean_sales) > 2 * std_sales,
    "Anomaly",
    "Normal"
)

fig4 = px.scatter(
    daily_df,
    x="Date",
    y="Daily_Sales",
    color="Anomaly",
    title="Sales Anomaly Detection"
)

fig4.update_layout(template="plotly_white")
st.plotly_chart(fig4, use_container_width=True)

# -------------------------------------------------
# Executive Insight
# -------------------------------------------------
st.success(
    """
🧠 **Executive Insights**

• Rolling averages smooth volatility and expose **true demand direction**  
• Day-of-week seasonality helps optimize **route planning & manpower**  
• Peak/low flags enable **proactive inventory & logistics decisions**  
• Anomalies highlight potential **supply disruption or reporting issues**
"""
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Advanced Daily Intelligence • DS Group FMCG Analytics Platform")
