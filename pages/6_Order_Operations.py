# pages/6_Pricing_Discount_Analysis.py
# -------------------------------------------------
# Pricing & Discount Analysis
# -------------------------------------------------

import streamlit as st
import pandas as pd

from utils.column_detector import auto_detect_columns
from utils.metrics import kpi_total_sales
from utils.visualizations import bar_top

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
    st.warning("📤 Please upload dataset or connect Snowflake.")
    st.stop()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

required = ["sales", "price"]
missing = [c for c in required if not cols.get(c)]

if missing:
    st.error(f"❌ Required columns missing: {missing}")
    st.stop()

discount_col = cols.get("discount")
product_col = cols.get("product") or cols.get("sku") or cols.get("brand")

# -------------------------------------------------
# Base KPIs
# -------------------------------------------------
k1, k2, k3 = st.columns(3)

k1.metric(
    "💰 Total Sales",
    f"{kpi_total_sales(df, cols['sales']):,.0f}"
)

k2.metric(
    "🏷 Avg Price",
    f"{df[cols['price']].mean():,.2f}"
)

if discount_col:
    k3.metric(
        "🔻 Avg Discount %",
        f"{df[discount_col].mean():.2f}%"
    )
else:
    k3.metric("🔻 Avg Discount %", "N/A")

st.divider()

# -------------------------------------------------
# Discount Impact Analysis
# -------------------------------------------------
if discount_col:
    st.subheader("📊 Discount vs Sales Impact")

    discount_bins = pd.cut(
        df[discount_col],
        bins=[-1, 0, 5, 10, 20, 50, 100],
        labels=["0%", "0–5%", "5–10%", "10–20%", "20–50%", "50%+"]
    )

    discount_summary = (
        df.assign(Discount_Band=discount_bins)
        .groupby("Discount_Band", observed=True)[cols["sales"]]
        .sum()
        .reset_index()
    )

    st.bar_chart(
        discount_summary.set_index("Discount_Band"),
        use_container_width=True
    )

    st.info(
        "📌 **Insight:** Excessive discounting may increase volume but can "
        "negatively impact profitability."
    )

else:
    st.warning("⚠ Discount column not detected. Discount analysis skipped.")

st.divider()

# -------------------------------------------------
# Top Products by Price or Sales
# -------------------------------------------------
if product_col:
    st.subheader("🏆 Top Products by Sales Value")

    st.plotly_chart(
        bar_top(
            df,
            product_col,
            cols["sales"],
            title="Top Products by Sales",
            top_n=15
        ),
        use_container_width=True
    )
else:
    st.warning("⚠ Product / SKU / Brand column not found.")

# -------------------------------------------------
# Price Distribution
# -------------------------------------------------
st.subheader("📈 Price Distribution")

st.line_chart(
    df[cols["price"]].value_counts().sort_index(),
    use_container_width=True
)

st.caption(
    "📌 Distribution highlights pricing spread and potential clustering "
    "around key price points."
)
