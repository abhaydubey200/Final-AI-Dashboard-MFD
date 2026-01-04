import streamlit as st
import pandas as pd

from config import SESSION_DF_KEY, CURRENCY_SYMBOL
from utils.column_detector import auto_detect_columns
from utils.visualizations import (
    line_sales_trend,
    bar_top,
    scatter_price_qty,
    pie_chart,
)
from utils.data_processing import preprocess

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Sales Performance | FMCG Intelligence",
    layout="wide",
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Please upload data or connect Snowflake first.")
    st.stop()

# -------------------------------------------------
# Column Detection
# -------------------------------------------------
cols = auto_detect_columns(df)

date_col = cols.get("date")
sales_col = cols.get("sales")
qty_col = cols.get("quantity")
brand_col = cols.get("brand")
sku_col = cols.get("sku")
outlet_col = cols.get("outlet")

# -------------------------------------------------
# Preprocess
# -------------------------------------------------
df = preprocess(df, date_col)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("📈 Sales Performance Analysis")
st.markdown(
    "Detailed breakdown of **sales trends, product contribution, and outlet performance**."
)

st.divider()

# -------------------------------------------------
# FILTERS
# -------------------------------------------------
with st.expander("🎯 Filters", expanded=False):
    f1, f2, f3 = st.columns(3)

    with f1:
        if brand_col:
            brands = st.multiselect(
                "Brand",
                sorted(df[brand_col].dropna().unique())
            )
            if brands:
                df = df[df[brand_col].isin(brands)]

    with f2:
        if outlet_col:
            outlets = st.multiselect(
                "Outlet",
                sorted(df[outlet_col].dropna().unique())
            )
            if outlets:
                df = df[df[outlet_col].isin(outlets)]

    with f3:
        if "Year" in df.columns:
            years = st.multiselect(
                "Year",
                sorted(df["Year"].unique())
            )
            if years:
                df = df[df["Year"].isin(years)]

# -------------------------------------------------
# SALES TREND
# -------------------------------------------------
st.markdown("## 📊 Sales Trend")

trend_fig = line_sales_trend(df, date_col, sales_col)
st.plotly_chart(trend_fig, use_container_width=True)

# -------------------------------------------------
# CONTRIBUTION ANALYSIS
# -------------------------------------------------
st.markdown("## 🧩 Contribution Analysis")

c1, c2 = st.columns(2)

with c1:
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

with c2:
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

# -------------------------------------------------
# OUTLET PERFORMANCE
# -------------------------------------------------
st.markdown("## 🏪 Outlet Performance")

o1, o2 = st.columns(2)

with o1:
    if outlet_col:
        st.plotly_chart(
            bar_top(
                df,
                outlet_col,
                sales_col,
                title="Top Outlets by Sales"
            ),
            use_container_width=True
        )

with o2:
    if outlet_col:
        outlet_share = (
            df.groupby(outlet_col, as_index=False)[sales_col]
            .sum()
            .sort_values(sales_col, ascending=False)
            .head(10)
        )
        st.plotly_chart(
            pie_chart(
                outlet_share,
                outlet_col,
                sales_col,
                title="Outlet Sales Share (Top 10)"
            ),
            use_container_width=True
        )

# -------------------------------------------------
# PRICE vs QUANTITY INSIGHTS
# -------------------------------------------------
st.markdown("## 💰 Price vs Quantity Behavior")

if sales_col and qty_col:
    st.plotly_chart(
        scatter_price_qty(
            df,
            sales_col,
            qty_col,
            title="Sales Value vs Quantity"
        ),
        use_container_width=True
    )
else:
    st.info("Quantity or Sales column not available for scatter analysis.")

# -------------------------------------------------
# EXECUTIVE INSIGHTS
# -------------------------------------------------
st.markdown("## 🧠 Key Business Insights")

insight_1 = "Sales momentum is driven by a small set of top-performing brands and outlets."
insight_2 = "Long-tail SKUs contribute marginally and may require rationalization."
insight_3 = "Higher quantity does not always correlate with higher sales value."

st.success(f"""
• {insight_1}  
• {insight_2}  
• {insight_3}
""")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Sales Performance • FMCG Executive Dashboard • DS Group")
