# pages/2_Sales_Performance.py
# -------------------------------------------------
# Sales Performance Dashboard
# -------------------------------------------------

import streamlit as st
import pandas as pd

from utils.column_detector import auto_detect_columns
from utils.visualizations import (
    line_sales_trend,
    bar_top,
    heatmap
)
from utils.metrics import (
    kpi_total_sales,
    kpi_orders,
    kpi_aov
)

st.set_page_config(
    page_title="Sales Performance",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Performance Analysis")
st.caption("In-depth sales trends, contribution & performance drivers")

st.divider()

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("📤 Please upload dataset or connect Snowflake first")
    st.stop()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

required = ["date", "sales"]
missing = [c for c in required if not cols.get(c)]

if missing:
    st.error(f"❌ Required columns missing: {', '.join(missing)}")
    st.stop()

# -------------------------------------------------
# Date Handling (INLINE & SAFE)
# -------------------------------------------------
df = df.copy()
df[cols["date"]] = pd.to_datetime(df[cols["date"]], errors="coerce")
df = df.dropna(subset=[cols["date"]])

# -------------------------------------------------
# KPIs
# -------------------------------------------------
k1, k2, k3 = st.columns(3)

k1.metric(
    "💰 Total Sales",
    f"{kpi_total_sales(df, cols['sales']):,.0f}"
)

k2.metric(
    "🧾 Total Orders",
    f"{kpi_orders(df):,}"
)

k3.metric(
    "📊 Avg Order Value",
    f"{kpi_aov(df, cols['sales']):,.0f}"
)

st.divider()

# -------------------------------------------------
# Time Trend
# -------------------------------------------------
st.subheader("📈 Sales Trend Over Time")

st.plotly_chart(
    line_sales_trend(
        df,
        cols["date"],
        cols["sales"],
        title="Sales Trend"
    ),
    use_container_width=True
)

# -------------------------------------------------
# Category / Brand Contribution
# -------------------------------------------------
if cols.get("brand"):
    st.subheader("🏷️ Brand Contribution")

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

# -------------------------------------------------
# City / State Heatmap
# -------------------------------------------------
geo_x = cols.get("state") or cols.get("city")
geo_y = cols.get("brand")

if geo_x and geo_y:
    st.subheader("🌍 Geographic Performance Heatmap")

    st.plotly_chart(
        heatmap(
            df,
            geo_x,
            geo_y,
            cols["sales"],
            title="Sales Distribution Heatmap"
        ),
        use_container_width=True
    )

# -------------------------------------------------
# Data Preview
# -------------------------------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(df.head(100), use_container_width=True)
