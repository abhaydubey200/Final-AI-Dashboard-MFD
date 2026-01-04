# -------------------------------------------------
# Page 1 : Executive Overview (CEO Dashboard)
# -------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np

from config import (
    SESSION_DF_KEY,
    CURRENCY_SYMBOL
)

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Executive Overview",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Executive Overview")
st.caption("CEO-level snapshot of FMCG business performance")

st.divider()

# -------------------------------------------------
# Load Data Safely
# -------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("Please upload data or connect Snowflake first.")
    st.stop()

# -------------------------------------------------
# Column Detection (SAFE)
# -------------------------------------------------
def find_col(possible):
    for c in possible:
        if c in df.columns:
            return c
    return None

sales_col = find_col(["sales", "total_sales", "revenue", "net_sales"])
qty_col = find_col(["quantity", "qty", "units"])
order_col = find_col(["order_id", "invoice_no", "bill_no"])
date_col = find_col(["date", "order_date", "invoice_date"])

# -------------------------------------------------
# KPI Calculations (ZERO RISK)
# -------------------------------------------------
total_sales = df[sales_col].sum() if sales_col else 0
total_orders = df[order_col].nunique() if order_col else len(df)
total_qty = df[qty_col].sum() if qty_col else 0

aov = (
    total_sales / total_orders
    if total_orders > 0 else 0
)

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "💰 Total Sales",
    f"{CURRENCY_SYMBOL}{total_sales:,.0f}"
)

c2.metric(
    "🧾 Total Orders",
    f"{total_orders:,}"
)

c3.metric(
    "📦 Total Volume",
    f"{total_qty:,.0f}"
)

c4.metric(
    "📈 Avg Order Value",
    f"{CURRENCY_SYMBOL}{aov:,.0f}"
)

st.divider()

# -------------------------------------------------
# AI EXECUTIVE SUMMARY (RULE-BASED)
# -------------------------------------------------
st.subheader("🧠 AI Executive Summary")

summary = []

if total_sales > 0:
    summary.append(
        f"Overall revenue stands at {CURRENCY_SYMBOL}{total_sales:,.0f}, "
        "indicating active sales performance."
    )

if aov > 0:
    summary.append(
        f"Average order value is {CURRENCY_SYMBOL}{aov:,.0f}, "
        "reflecting current pricing and basket size."
    )

if total_orders > 0:
    summary.append(
        f"Business processed {total_orders:,} orders in the selected dataset."
    )

if not summary:
    summary.append(
        "Insufficient data available to generate insights."
    )

for line in summary:
    st.markdown(f"- {line}")

# -------------------------------------------------
# DATA PREVIEW (CEO Friendly)
# -------------------------------------------------
with st.expander("📄 Data Preview", expanded=False):
    st.dataframe(df.head(50), use_container_width=True)
