import streamlit as st
import pandas as pd

from config import SESSION_DF_KEY, CURRENCY_SYMBOL
from utils.column_detector import auto_detect_columns
from utils.data_processing import preprocess
from utils.metrics import top_contributors
from utils.pricing_metrics import sku_price_metrics
from utils.visualizations import (
    bar_top,
    pie_chart,
    scatter_price_qty,
)

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Product • SKU • Brand Analysis",
    layout="wide",
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Upload data or connect Snowflake to continue.")
    st.stop()

# -------------------------------------------------
# Column Detection
# -------------------------------------------------
cols = auto_detect_columns(df)

brand_col = cols.get("brand")
sku_col = cols.get("sku")
sales_col = cols.get("sales")
qty_col = cols.get("quantity")
date_col = cols.get("date")

# -------------------------------------------------
# Preprocess
# -------------------------------------------------
df = preprocess(df, date_col)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("📦 Product / SKU / Brand Performance")
st.markdown(
    "Analyze **brand dominance, SKU efficiency, and pricing behavior** "
    "to drive portfolio optimization."
)

st.divider()

# -------------------------------------------------
# FILTERS
# -------------------------------------------------
with st.expander("🎯 Filters", expanded=False):
    f1, f2 = st.columns(2)

    with f1:
        if brand_col:
            brands = st.multiselect(
                "Brand",
                sorted(df[brand_col].dropna().unique())
            )
            if brands:
                df = df[df[brand_col].isin(brands)]

    with f2:
        if "Year" in df.columns:
            years = st.multiselect(
                "Year",
                sorted(df["Year"].unique())
            )
            if years:
                df = df[df["Year"].isin(years)]

# -------------------------------------------------
# BRAND PERFORMANCE
# -------------------------------------------------
st.markdown("## 🏷 Brand Performance")

b1, b2 = st.columns(2)

with b1:
    if brand_col:
        st.plotly_chart(
            bar_top(
                df,
                brand_col,
                sales_col,
                title="Top Brands by Sales"
            ),
            use_container_width=True
        )

with b2:
    if brand_col:
        brand_share = top_contributors(
            df,
            brand_col,
            sales_col,
            top_n=8
        )
        st.plotly_chart(
            pie_chart(
                brand_share,
                brand_col,
                sales_col,
                title="Brand Sales Share"
            ),
            use_container_width=True
        )

# -------------------------------------------------
# SKU PERFORMANCE
# -------------------------------------------------
st.markdown("## 🧾 SKU Performance")

s1, s2 = st.columns(2)

with s1:
    if sku_col:
        st.plotly_chart(
            bar_top(
                df,
                sku_col,
                sales_col,
                title="Top SKUs by Sales"
            ),
            use_container_width=True
        )

with s2:
    if sku_col:
        st.plotly_chart(
            bar_top(
                df,
                sku_col,
                qty_col,
                title="Top SKUs by Quantity"
            ),
            use_container_width=True
        )

# -------------------------------------------------
# PRICE vs QUANTITY INTELLIGENCE
# -------------------------------------------------
st.markdown("## 💰 Price vs Quantity Intelligence")

if sales_col and qty_col:
    st.plotly_chart(
        scatter_price_qty(
            df,
            sales_col,
            qty_col,
            title="Revenue vs Volume (SKU Level)"
        ),
        use_container_width=True
    )
else:
    st.info("Sales or Quantity column missing for price-volume analysis.")

# -------------------------------------------------
# SKU PRICING METRICS
# -------------------------------------------------
st.markdown("## 📊 SKU Pricing Metrics")

if sku_col:
    pricing_df = sku_price_metrics(df)

    st.dataframe(
        pricing_df.head(20),
        use_container_width=True
    )

# -------------------------------------------------
# EXECUTIVE INSIGHTS
# -------------------------------------------------
st.markdown("## 🧠 Executive Insights")

st.success(
    """
• A small number of brands contribute majority of revenue → **concentration risk**  
• Several SKUs show high volume but low value → **pricing or discount issue**  
• Low-volume & low-value SKUs indicate **portfolio rationalization opportunity**  
"""
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Product & SKU Intelligence • FMCG Executive Dashboard • DS Group")
