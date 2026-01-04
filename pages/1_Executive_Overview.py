# -------------------------------------------------
# Page 1 : Executive Overview
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

st.header("🧠 Executive Overview")
st.caption("High-level FMCG business performance snapshot")

st.divider()

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("📤 Upload dataset or connect Snowflake first")
    st.stop()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

required_cols = ["date", "sales"]
missing = [c for c in required_cols if not cols.get(c)]

if missing:
    st.error(f"❌ Required columns not detected: {', '.join(missing)}")
    st.stop()

# -------------------------------------------------
# SAFE PREPROCESS (INLINE – CLOUD SAFE)
# -------------------------------------------------
try:
    df[cols["date"]] = pd.to_datetime(df[cols["date"]])
except Exception:
    st.error("❌ Date column cannot be parsed")
    st.stop()

df = df.sort_values(cols["date"])

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "💰 Total Sales",
        f"{kpi_total_sales(df, cols['sales']):,.0f}"
    )

with c2:
    st.metric(
        "🧾 Orders",
        f"{kpi_orders(df):,}"
    )

with c3:
    st.metric(
        "📈 Avg Order Value",
        f"{kpi_aov(df, cols['sales']):,.0f}"
    )

st.divider()

# -------------------------------------------------
# Sales Trend
# -------------------------------------------------
st.subheader("📊 Sales Trend")

st.plotly_chart(
    line_sales_trend(
        df,
        cols["date"],
        cols["sales"]
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
            "Top Brands"
        ),
        use_container_width=True
    )
else:
    st.info("ℹ️ Brand column not found — skipping brand analysis")

# -------------------------------------------------
# Preview
# -------------------------------------------------
with st.expander("📄 Data Preview"):
    st.dataframe(df.head(50), use_container_width=True)
