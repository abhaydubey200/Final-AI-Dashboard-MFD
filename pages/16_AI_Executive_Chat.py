import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from config import (
    SESSION_DF_KEY,
    CURRENCY_SYMBOL,
    NUMBER_FORMAT,
)

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="AI Executive Assistant",
    layout="wide",
)

# =================================================
# LOAD DATA
# =================================================
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Upload dataset first to activate AI Executive Assistant.")
    st.stop()

# =================================================
# STANDARDIZE COLUMNS
# =================================================
df.columns = [c.upper() for c in df.columns]

# =================================================
# HEADER
# =================================================
st.markdown(
    """
    <div style="padding:18px;border-radius:14px;background:#F5F7FA">
        <h2>🧠 AI Executive Assistant</h2>
        <p style="color:#333">
            Enterprise decision intelligence • Boardroom-ready • DS Group AI
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# =================================================
# AUTO-SUGGEST QUESTION CHIPS
# =================================================
st.markdown("### 💡 Suggested Executive Questions")

SUGGESTED_QUESTIONS = [
    "Total sales",
    "Overall business performance",
    "Sales by month",
    "Top SKUs by revenue",
    "Outlet inactivity risk",
    "Revenue concentration risk",
    "Rejected orders summary",
    "Discount impact on revenue",
    "Best performing zone",
    "Worst performing outlet",
]

chip_cols = st.columns(len(SUGGESTED_QUESTIONS))

selected_question = None
for i, q in enumerate(SUGGESTED_QUESTIONS):
    if chip_cols[i].button(q):
        selected_question = q

st.divider()

# =================================================
# USER QUESTION INPUT
# =================================================
user_question = st.text_input(
    "Ask any question about your business data",
    value=selected_question if selected_question else "",
    placeholder="e.g. total sales, outlet risk, sku performance",
)

if not user_question:
    st.stop()

q = user_question.lower()

# =================================================
# HELPER FUNCTIONS
# =================================================
def format_currency(val):
    return f"{CURRENCY_SYMBOL}{val:,.0f}"

def executive_note():
    st.caption(
        "Executive Note: This insight is derived directly from current dataset signals "
        "and is suitable for leadership decision-making."
    )

# =================================================
# INTENT ENGINE (RULE-BASED)
# =================================================
st.markdown("### 📊 Executive Intelligence Output")

# -------------------------------------------------
# TOTAL SALES
# -------------------------------------------------
if "total sales" in q or "revenue" in q:
    total_sales = df["AMOUNT"].sum()

    st.success("📊 Total Sales Overview")
    st.metric("Total Recorded Sales", format_currency(total_sales))
    executive_note()

# -------------------------------------------------
# TOTAL ORDERS
# -------------------------------------------------
elif "total orders" in q or "order count" in q:
    total_orders = df["ORDER_ID"].nunique()

    st.success("📦 Order Volume Summary")
    st.metric("Total Orders", f"{total_orders:,}")
    executive_note()

# -------------------------------------------------
# OVERALL PERFORMANCE
# -------------------------------------------------
elif "performance" in q or "business performance" in q:
    sales = df["AMOUNT"].sum()
    orders = df["ORDER_ID"].nunique()
    outlets = df["OUTLET_ID"].nunique()

    st.success("📊 Overall Business Performance")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", format_currency(sales))
    col2.metric("Orders", f"{orders:,}")
    col3.metric("Active Outlets", f"{outlets:,}")

    executive_note()

# -------------------------------------------------
# SALES BY MONTH
# -------------------------------------------------
elif "sales by month" in q or "monthly sales" in q:
    df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"])
    monthly = (
        df.groupby(df["ORDER_DATE"].dt.to_period("M"))["AMOUNT"]
        .sum()
        .reset_index()
    )

    st.success("📈 Monthly Sales Performance")
    st.dataframe(monthly.rename(columns={"AMOUNT": "Monthly Sales"}))
    executive_note()

# -------------------------------------------------
# TOP SKUS
# -------------------------------------------------
elif "top sku" in q or "sku performance" in q:
    sku_perf = (
        df.groupby("SKU_PLACED")["AMOUNT"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.success("🏆 Top SKUs by Revenue")
    st.dataframe(sku_perf.reset_index())
    executive_note()

# -------------------------------------------------
# OUTLET INACTIVITY
# -------------------------------------------------
elif "outlet inactivity" in q or "inactive outlet" in q:
    df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"])
    last_date = df["ORDER_DATE"].max()
    last_order = df.groupby("OUTLET_ID")["ORDER_DATE"].max()
    inactive = last_order[last_order < last_date - pd.Timedelta(days=30)]

    st.warning("⚠️ Outlet Inactivity Risk Detected")
    st.metric("Inactive Outlets (>30 days)", len(inactive))
    executive_note()

# -------------------------------------------------
# REVENUE CONCENTRATION
# -------------------------------------------------
elif "concentration" in q or "dependency" in q:
    sku_sales = df.groupby("SKU_PLACED")["AMOUNT"].sum()
    top_share = sku_sales.max() / sku_sales.sum() * 100

    st.warning("⚠️ Revenue Concentration Risk")
    st.metric("Top SKU Contribution (%)", f"{top_share:.1f}%")
    executive_note()

# -------------------------------------------------
# REJECTED ORDERS
# -------------------------------------------------
elif "rejected" in q:
    rejected = df[df["ORDERSTATE"].str.contains("reject", case=False, na=False)]
    rate = len(rejected) / len(df) * 100

    st.warning("🚫 Order Rejection Summary")
    st.metric("Rejection Rate", f"{rate:.2f}%")
    executive_note()

# -------------------------------------------------
# DISCOUNT IMPACT
# -------------------------------------------------
elif "discount" in q:
    total_discount = df["DISCOUNT_AMOUNT"].sum()
    total_sales = df["AMOUNT"].sum()

    st.info("💸 Discount Impact Analysis")
    st.metric("Total Discount Given", format_currency(total_discount))
    st.metric("Discount % of Sales", f"{(total_discount/total_sales)*100:.2f}%")
    executive_note()

# -------------------------------------------------
# FALLBACK
# -------------------------------------------------
else:
    st.info("📊 Executive intelligence ready")
    st.markdown(
        """
        Try asking about:
        - Sales
        - Orders
        - SKUs
        - Outlets
        - Risks
        - Performance
        """
    )
    executive_note()
