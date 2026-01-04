import streamlit as st
import pandas as pd

from config import SESSION_DF_KEY
from utils.column_detector import auto_detect_columns
from utils.data_processing import preprocess
from utils.metrics import top_contributors
from utils.warehouse_metrics import outlet_distribution_metrics
from utils.visualizations import bar_top, pie_chart

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Outlet Distribution & Coverage",
    layout="wide",
)

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Upload data or connect Snowflake to continue.")
    st.stop()

# -------------------------------------------------
# Auto Column Detection
# -------------------------------------------------
cols = auto_detect_columns(df)

outlet_col = cols.get("outlet")
city_col = cols.get("city")
warehouse_col = cols.get("warehouse")
sales_col = cols.get("sales")
date_col = cols.get("date")

# -------------------------------------------------
# Preprocess
# -------------------------------------------------
df = preprocess(df, date_col)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("🏪 Outlet Distribution & Market Coverage")
st.markdown(
    "Evaluate **outlet reach, geographic dominance, and distribution risk** "
    "to strengthen FMCG supply strategy."
)

st.divider()

# -------------------------------------------------
# FILTERS
# -------------------------------------------------
with st.expander("🎯 Filters", expanded=False):
    c1, c2 = st.columns(2)

    with c1:
        if city_col:
            cities = st.multiselect(
                "City",
                sorted(df[city_col].dropna().unique())
            )
            if cities:
                df = df[df[city_col].isin(cities)]

    with c2:
        if warehouse_col:
            warehouses = st.multiselect(
                "Warehouse",
                sorted(df[warehouse_col].dropna().unique())
            )
            if warehouses:
                df = df[df[warehouse_col].isin(warehouses)]

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.markdown("## 📌 Distribution KPIs")

k1, k2, k3 = st.columns(3)

total_outlets = df[outlet_col].nunique() if outlet_col else 0
total_cities = df[city_col].nunique() if city_col else 0
total_warehouses = df[warehouse_col].nunique() if warehouse_col else 0

k1.metric("🏪 Total Active Outlets", f"{total_outlets:,}")
k2.metric("🌆 Cities Covered", f"{total_cities:,}")
k3.metric("🏭 Warehouses", f"{total_warehouses:,}")

st.divider()

# -------------------------------------------------
# CITY LEVEL DISTRIBUTION
# -------------------------------------------------
st.markdown("## 🌆 City-wise Outlet Coverage")

if city_col and outlet_col:
    city_outlets = (
        df.groupby(city_col)[outlet_col]
        .nunique()
        .reset_index(name="Outlet Count")
        .sort_values("Outlet Count", ascending=False)
    )

    c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(
            bar_top(
                city_outlets,
                city_col,
                "Outlet Count",
                title="Top Cities by Outlet Count"
            ),
            use_container_width=True
        )

    with c2:
        st.plotly_chart(
            pie_chart(
                city_outlets.head(8),
                city_col,
                "Outlet Count",
                title="Outlet Share by City"
            ),
            use_container_width=True
        )

# -------------------------------------------------
# WAREHOUSE DISTRIBUTION
# -------------------------------------------------
st.markdown("## 🏭 Warehouse-wise Distribution")

if warehouse_col and sales_col:
    warehouse_metrics = outlet_distribution_metrics(df)

    w1, w2 = st.columns(2)

    with w1:
        st.plotly_chart(
            bar_top(
                warehouse_metrics,
                warehouse_col,
                "Total_Sales",
                title="Warehouse Sales Contribution"
            ),
            use_container_width=True
        )

    with w2:
        st.dataframe(
            warehouse_metrics,
            use_container_width=True
        )

# -------------------------------------------------
# DEPENDENCY RISK
# -------------------------------------------------
st.markdown("## ⚠ Distribution Dependency Risk")

if city_col and sales_col:
    city_sales = top_contributors(
        df,
        city_col,
        sales_col,
        top_n=5
    )

    st.plotly_chart(
        pie_chart(
            city_sales,
            city_col,
            sales_col,
            title="Top 5 Cities – Revenue Dependency"
        ),
        use_container_width=True
    )

    st.warning(
        "⚠ Heavy revenue dependency on limited cities increases operational risk."
    )

# -------------------------------------------------
# EXECUTIVE INSIGHTS
# -------------------------------------------------
st.markdown("## 🧠 Executive Insights")

st.success(
    """
• Uneven outlet concentration suggests **white-space expansion opportunities**  
• High dependency on select cities/warehouses → **supply chain risk**  
• Optimizing outlet mix improves **service levels & revenue stability**
"""
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Outlet Distribution Intelligence • FMCG Executive Dashboard • DS Group")
