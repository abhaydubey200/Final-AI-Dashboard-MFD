import streamlit as st
import pandas as pd

from config import SESSION_DF_KEY
from utils.column_detector import auto_detect_columns
from utils.metrics import order_operation_metrics
from utils.warehouse_metrics import warehouse_kpis
from utils.visualizations import bar_top

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Order Operations",
    layout="wide"
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Upload data or connect Snowflake to continue.")
    st.stop()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

order_col = cols.get("order")
sales_col = cols.get("sales")
qty_col = cols.get("quantity")
warehouse_col = cols.get("warehouse")
outlet_col = cols.get("outlet")
date_col = cols.get("date")

required = [order_col, sales_col, qty_col]
if not all(required):
    st.error("❌ Required order / sales / quantity columns not detected")
    st.stop()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("📦 Order Operations & Fulfilment Intelligence")
st.markdown(
    "Monitor **order flow, quantity movement, warehouse efficiency, "
    "and operational risks** across FMCG supply chain."
)

st.divider()

# -------------------------------------------------
# FILTERS
# -------------------------------------------------
with st.expander("🎯 Filters", expanded=False):
    c1, c2 = st.columns(2)

    with c1:
        if warehouse_col:
            wh = st.multiselect(
                "Warehouse",
                sorted(df[warehouse_col].dropna().unique())
            )
            if wh:
                df = df[df[warehouse_col].isin(wh)]

    with c2:
        if outlet_col:
            outlets = st.multiselect(
                "Outlet",
                sorted(df[outlet_col].dropna().unique())
            )
            if outlets:
                df = df[df[outlet_col].isin(outlets)]

# -------------------------------------------------
# ORDER METRICS
# -------------------------------------------------
ops_df = order_operation_metrics(
    df,
    order_col=order_col,
    sales_col=sales_col,
    qty_col=qty_col
)

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.markdown("## 📌 Order KPIs")

k1, k2, k3, k4 = st.columns(4)

k1.metric("📑 Total Orders", f"{ops_df['Total_Orders']:,}")
k2.metric("📦 Total Quantity", f"{ops_df['Total_Quantity']:,.0f}")
k3.metric("💰 Total Sales", f"{ops_df['Total_Sales']:,.0f}")
k4.metric("⚠ Avg Qty / Order", f"{ops_df['Avg_Qty_Per_Order']:.1f}")

st.divider()

# -------------------------------------------------
# WAREHOUSE PERFORMANCE
# -------------------------------------------------
if warehouse_col:
    st.markdown("## 🏭 Warehouse Operations Performance")

    wh_df = warehouse_kpis(
        df,
        warehouse_col=warehouse_col,
        sales_col=sales_col,
        qty_col=qty_col
    )

    c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(
            bar_top(
                wh_df,
                warehouse_col,
                "Total_Sales",
                title="Warehouse Sales Contribution"
            ),
            use_container_width=True
        )

    with c2:
        st.plotly_chart(
            bar_top(
                wh_df,
                warehouse_col,
                "Total_Quantity",
                title="Warehouse Quantity Movement"
            ),
            use_container_width=True
        )

    st.dataframe(wh_df, use_container_width=True)

st.divider()

# -------------------------------------------------
# LEAKAGE & RISK
# -------------------------------------------------
st.markdown("## ⚠ Operational Risk Indicators")

risk_df = df.groupby(order_col).agg(
    Quantity=("{}".format(qty_col), "sum"),
    Sales=("{}".format(sales_col), "sum")
).reset_index()

risk_df["Sales_per_Unit"] = risk_df["Sales"] / risk_df["Quantity"]

low_eff = risk_df[
    risk_df["Sales_per_Unit"] < risk_df["Sales_per_Unit"].median()
]

st.dataframe(low_eff.sort_values("Sales_per_Unit"), use_container_width=True)

st.warning(
    "⚠ Orders with low sales per unit may indicate discount leakage, "
    "wrong assortment, or fulfilment inefficiency."
)

# -------------------------------------------------
# EXECUTIVE INSIGHTS
# -------------------------------------------------
st.markdown("## 🧠 Executive Insights")

st.success(
    """
• High order count does not always mean high revenue  
• Warehouse imbalance increases logistics cost  
• Monitoring sales-per-unit prevents margin erosion  
"""
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Order Operations Intelligence • DS Group FMCG Dashboard")
