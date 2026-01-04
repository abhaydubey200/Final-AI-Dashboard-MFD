# pages/4_Outlet_Distribution.py
# -------------------------------------------------
# Outlet Distribution & Coverage Analysis
# -------------------------------------------------

import streamlit as st
import pandas as pd

from utils.column_detector import auto_detect_columns
from utils.metrics import (
    kpi_total_sales,
    kpi_orders,
)
from utils.visualizations import (
    bar_top
)

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Outlet Distribution | DS Group",
    page_icon="🏪",
    layout="wide"
)

st.title("🏪 Outlet Distribution & Coverage")
st.caption("Analyze outlet contribution, coverage strength & concentration")

st.divider()

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("📤 Please upload dataset or connect Snowflake.")
    st.stop()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

required = ["outlet", "sales", "date"]
missing = [c for c in required if not cols.get(c)]

if missing:
    st.error(f"❌ Required columns missing: {missing}")
    st.stop()

# -------------------------------------------------
# Safe Date Handling
# -------------------------------------------------
df = df.copy()
df[cols["date"]] = pd.to_datetime(df[cols["date"]], errors="coerce")
df = df.dropna(subset=[cols["date"]])

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
k1, k2, k3 = st.columns(3)

k1.metric(
    "🏪 Total Outlets",
    f"{df[cols['outlet']].nunique():,}"
)

k2.metric(
    "💰 Total Sales",
    f"{kpi_total_sales(df, cols['sales']):,.0f}"
)

k3.metric(
    "🧾 Total Orders",
    f"{kpi_orders(df):,}"
)

st.divider()

# -------------------------------------------------
# Outlet Contribution
# -------------------------------------------------
st.subheader("📊 Top Outlets by Sales")

st.plotly_chart(
    bar_top(
        df,
        cols["outlet"],
        cols["sales"],
        title="Top Performing Outlets",
        top_n=20
    ),
    use_container_width=True
)

# -------------------------------------------------
# Outlet Concentration Insight
# -------------------------------------------------
st.subheader("📈 Outlet Sales Concentration")

outlet_sales = (
    df.groupby(cols["outlet"])[cols["sales"]]
    .sum()
    .sort_values(ascending=False)
)

top_20_share = (
    outlet_sales.head(20).sum() / outlet_sales.sum()
) * 100

st.metric(
    "Top 20 Outlets Contribution",
    f"{top_20_share:.2f}%"
)

st.info(
    "📌 **Insight:** High concentration indicates dependency on a limited number "
    "of outlets. Diversifying outlet contribution reduces revenue risk."
)

# -------------------------------------------------
# Outlet-Level Table
# -------------------------------------------------
with st.expander("📄 Outlet Sales Table"):
    outlet_table = (
        df.groupby(cols["outlet"], as_index=False)[cols["sales"]]
        .sum()
        .rename(columns={cols["sales"]: "Total_Sales"})
        .sort_values("Total_Sales", ascending=False)
    )

    st.dataframe(outlet_table, use_container_width=True)
