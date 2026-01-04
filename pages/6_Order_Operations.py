# pages/6_Pricing_Analysis.py
# -------------------------------------------------
# Pricing & Discount Analysis
# -------------------------------------------------

import streamlit as st
from utils.column_detector import auto_detect_columns
from utils.pricing_metrics import *
from utils.visualizations import *

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Pricing & Discount Analysis | DS Group",
    page_icon="💸",
    layout="wide"
)

st.title("💸 Pricing & Discount Analysis")
st.caption("Analyze discount impact on sales & pricing effectiveness")

st.divider()

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("📤 Upload dataset or connect Snowflake first.")
    st.stop()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

price_col = cols.get("price")
sales_col = cols.get("sales")
discount_col = cols.get("discount")
date_col = cols.get("date")

# -------------------------------------------------
# Validation (Backward Compatible)
# -------------------------------------------------
if not price_col:
    st.warning("⚠ Price column not detected — pricing analysis unavailable.")
    st.stop()

if not sales_col:
    st.warning("⚠ Sales column not detected.")
    st.stop()

# -------------------------------------------------
# KPIs
# -------------------------------------------------
st.subheader("📊 Pricing KPIs")

k1, k2, k3 = st.columns(3)

k1.metric(
    "Average Selling Price",
    f"₹{avg_price(df, price_col):,.2f}"
)

if discount_col:
    k2.metric(
        "Average Discount %",
        f"{avg_discount(df, discount_col):.2f}%"
    )
else:
    k2.metric("Average Discount %", "N/A")

k3.metric(
    "Revenue Impact",
    f"₹{revenue_impact(df, price_col, sales_col):,.0f}"
)

# -------------------------------------------------
# Price Distribution
# -------------------------------------------------
st.subheader("📈 Price Distribution")

st.plotly_chart(
    price_distribution(df, price_col),
    use_container_width=True
)

# -------------------------------------------------
# Discount Impact
# -------------------------------------------------
if discount_col:
    st.subheader("🎯 Discount vs Sales Impact")

    st.plotly_chart(
        discount_vs_sales(df, discount_col, sales_col),
        use_container_width=True
    )
else:
    st.info("ℹ Discount column not available — skipping discount impact analysis.")

# -------------------------------------------------
# Trend Analysis
# -------------------------------------------------
if date_col:
    st.subheader("📆 Price Trend Over Time")

    st.plotly_chart(
        price_trend(df, date_col, price_col),
        use_container_width=True
    )

# -------------------------------------------------
# Business Insights
# -------------------------------------------------
st.info(
    "📌 **Insights:**\n\n"
    "- Detect price sensitivity and discount dependency\n"
    "- Optimize pricing strategy across products & outlets\n"
    "- Prevent margin erosion due to excessive discounting"
)
