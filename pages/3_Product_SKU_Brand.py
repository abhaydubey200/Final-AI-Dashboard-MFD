# pages/3_Product_SKU_Brand.py
# -------------------------------------------------
# Product / SKU / Brand Performance Dashboard
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
    bar_top,
    line_sales_trend
)

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Product & Brand Performance | DS Group",
    page_icon="🏷️",
    layout="wide"
)

st.title("🏷️ Product / SKU / Brand Performance")
st.caption("Deep dive into brand-level and SKU-level contribution")

st.divider()

# -------------------------------------------------
# Load Dataset (STANDARD)
# -------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("📤 Please upload dataset or connect Snowflake.")
    st.stop()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

required_cols = ["date", "sales"]
missing = [c for c in required_cols if not cols.get(c)]

if missing:
    st.error(f"❌ Required columns missing: {missing}")
    st.stop()

# -------------------------------------------------
# Safe Date Handling (INLINE)
# -------------------------------------------------
df = df.copy()
df[cols["date"]] = pd.to_datetime(df[cols["date"]], errors="coerce")
df = df.dropna(subset=[cols["date"]])

# -------------------------------------------------
# KPI SECTION
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
# Brand Performance
# -------------------------------------------------
if cols.get("brand"):
    st.subheader("🏷️ Top Brands by Sales")

    st.plotly_chart(
        bar_top(
            df,
            cols["brand"],
            cols["sales"],
            title="Top Brands",
            top_n=15
        ),
        use_container_width=True
    )

# -------------------------------------------------
# SKU Performance
# -------------------------------------------------
if cols.get("sku"):
    st.subheader("📦 Top SKUs by Sales")

    st.plotly_chart(
        bar_top(
            df,
            cols["sku"],
            cols["sales"],
            title="Top SKUs",
            top_n=15
        ),
        use_container_width=True
    )

# -------------------------------------------------
# Brand Sales Trend
# -------------------------------------------------
if cols.get("brand"):
    st.subheader("📈 Brand Sales Trend")

    selected_brand = st.selectbox(
        "Select Brand",
        sorted(df[cols["brand"]].dropna().unique())
    )

    brand_df = df[df[cols["brand"]] == selected_brand]

    st.plotly_chart(
        line_sales_trend(
            brand_df,
            cols["date"],
            cols["sales"],
            title=f"Sales Trend – {selected_brand}"
        ),
        use_container_width=True
    )

# -------------------------------------------------
# Data Preview
# -------------------------------------------------
with st.expander("📄 View Sample Data"):
    st.dataframe(df.head(100), use_container_width=True)
