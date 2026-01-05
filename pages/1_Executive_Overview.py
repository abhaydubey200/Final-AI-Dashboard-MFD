# pages/1_Executive_Overview.py
# -------------------------------------------------

import streamlit as st
import pandas as pd

from utils.column_detector import auto_detect_columns
from utils.metrics import (
    kpi_total_sales,
    kpi_orders,
    kpi_aov
)
from utils.visualizations import (
    line_sales_trend,
    bar_top
)

st.set_page_config(
    page_title="Executive Overview",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Executive Overview")
st.caption("snapshot of FMCG business performance")

st.divider()

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("📤 Upload dataset or connect Snowflake")
    st.stop()

# -------------------------------------------------
# Column Detection
# -------------------------------------------------
cols = auto_detect_columns(df)

required = ["date", "sales"]
missing = [c for c in required if not cols.get(c)]

if missing:
    st.error(f"❌ Missing required columns: {', '.join(missing)}")
    st.stop()

# -------------------------------------------------
# Date Handling (SAFE)
# -------------------------------------------------
df = df.copy()
df[cols["date"]] = pd.to_datetime(df[cols["date"]], errors="coerce")
df = df.dropna(subset=[cols["date"]])

# -------------------------------------------------
# KPIs
# -------------------------------------------------
c1, c2, c3 = st.columns(3)

c1.metric(
    "💰 Total Sales",
    f"{kpi_total_sales(df, cols['sales']):,.0f}"
)

c2.metric(
    "🧾 Orders",
    f"{kpi_orders(df):,}"
)

c3.metric(
    "📊 Avg Order Value",
    f"{kpi_aov(df, cols['sales']):,.0f}"
)

st.divider()

# -------------------------------------------------
# Sales Trend
# -------------------------------------------------
st.subheader("📈 Sales Trend")

st.plotly_chart(
    line_sales_trend(
        df,
        cols["date"],
        cols["sales"],
        title="Historical Sales Trend"
    ),
    use_container_width=True
)

# -------------------------------------------------
# Brand Performance
# -------------------------------------------------
if cols.get("brand"):
    st.subheader("🏷️ Top Brands")

    st.plotly_chart(
        bar_top(
            df,
            cols["brand"],
            cols["sales"],
            title="Top Brands by Sales",
            top_n=10
        ),
        use_container_width=True
    )
else:
    st.info("ℹ️ Brand column not detected")

# -------------------------------------------------
# Preview
# -------------------------------------------------
with st.expander("📄 Data Preview"):
    st.dataframe(df.head(50), use_container_width=True)
