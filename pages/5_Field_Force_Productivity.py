# pages/5_Field_Force_Productivity.py
# -------------------------------------------------
# Field Force Productivity Analysis
# -------------------------------------------------

import streamlit as st
import pandas as pd

from utils.column_detector import auto_detect_columns
from utils.metrics import (
    kpi_total_sales,
    kpi_orders,
)
from utils.visualizations import bar_top

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Field Force Productivity | DS Group",
    page_icon="🧑‍💼",
    layout="wide"
)

st.title("🧑‍💼 Field Force Productivity")
st.caption("Evaluate sales representative efficiency & contribution")

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

required = ["sales_rep", "sales", "date"]
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
    "🧑‍💼 Total Sales Reps",
    f"{df[cols['sales_rep']].nunique():,}"
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
# Sales Rep Performance
# -------------------------------------------------
st.subheader("📊 Top Performing Sales Representatives")

st.plotly_chart(
    bar_top(
        df,
        cols["sales_rep"],
        cols["sales"],
        title="Top Sales Representatives by Sales",
        top_n=20
    ),
    use_container_width=True
)

# -------------------------------------------------
# Productivity Metrics
# -------------------------------------------------
st.subheader("📈 Productivity Metrics")

rep_summary = (
    df.groupby(cols["sales_rep"])
    .agg(
        Total_Sales=(cols["sales"], "sum"),
        Orders=("Order_ID", "count") if "Order_ID" in df.columns else ("date", "count")
    )
    .reset_index()
)

rep_summary["Sales_per_Order"] = (
    rep_summary["Total_Sales"] / rep_summary["Orders"]
)

top_productive = rep_summary.sort_values(
    "Sales_per_Order", ascending=False
).head(10)

st.metric(
    "🏆 Best Avg Sales / Order",
    f"{top_productive.iloc[0]['Sales_per_Order']:,.0f}"
)

st.info(
    "📌 **Insight:** Higher sales per order reflects stronger negotiation, "
    "better route planning, or premium outlet coverage."
)

# -------------------------------------------------
# Detailed Rep Table
# -------------------------------------------------
with st.expander("📄 Sales Representative Productivity Table"):
    st.dataframe(
        rep_summary.sort_values("Total_Sales", ascending=False),
        use_container_width=True
    )
