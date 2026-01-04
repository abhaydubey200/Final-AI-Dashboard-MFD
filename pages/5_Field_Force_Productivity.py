import streamlit as st
import pandas as pd

from config import SESSION_DF_KEY
from utils.column_detector import auto_detect_columns
from utils.data_processing import preprocess
from utils.metrics import productivity_metrics
from utils.visualizations import bar_top, scatter_plot

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Field Force Productivity",
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

rep_col = cols.get("sales_rep") or cols.get("field_force")
outlet_col = cols.get("outlet")
sales_col = cols.get("sales")
date_col = cols.get("date")
city_col = cols.get("city")

if not rep_col or not outlet_col or not sales_col:
    st.error("❌ Field force, outlet, or sales column missing")
    st.stop()

# -------------------------------------------------
# Preprocess
# -------------------------------------------------
df = preprocess(df, date_col)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("🚴 Field Force Productivity & Efficiency")
st.markdown(
    "Measure **sales effectiveness, outlet coverage, and productivity risk** "
    "across your FMCG field force."
)

st.divider()

# -------------------------------------------------
# FILTERS
# -------------------------------------------------
with st.expander("🎯 Filters", expanded=False):
    c1, c2 = st.columns(2)

    with c1:
        reps = st.multiselect(
            "Sales Representative",
            sorted(df[rep_col].dropna().unique())
        )
        if reps:
            df = df[df[rep_col].isin(reps)]

    with c2:
        if city_col:
            cities = st.multiselect(
                "City",
                sorted(df[city_col].dropna().unique())
            )
            if cities:
                df = df[df[city_col].isin(cities)]

# -------------------------------------------------
# PRODUCTIVITY METRICS
# -------------------------------------------------
prod_df = productivity_metrics(
    df,
    rep_col=rep_col,
    outlet_col=outlet_col,
    sales_col=sales_col
)

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
st.markdown("## 📌 Productivity KPIs")

k1, k2, k3 = st.columns(3)

k1.metric("👥 Active Field Reps", f"{prod_df.shape[0]:,}")
k2.metric("🏪 Avg Outlets / Rep", f"{prod_df['Outlet_Count'].mean():.1f}")
k3.metric("💰 Avg Sales / Rep", f"{prod_df['Total_Sales'].mean():,.0f}")

st.divider()

# -------------------------------------------------
# TOP PERFORMERS
# -------------------------------------------------
st.markdown("## 🏆 Top Performing Field Reps")

c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(
        bar_top(
            prod_df,
            rep_col,
            "Total_Sales",
            title="Top Field Reps by Sales"
        ),
        use_container_width=True
    )

with c2:
    st.plotly_chart(
        bar_top(
            prod_df,
            rep_col,
            "Outlet_Count",
            title="Top Field Reps by Outlet Coverage"
        ),
        use_container_width=True
    )

# -------------------------------------------------
# PRODUCTIVITY SCATTER
# -------------------------------------------------
st.markdown("## 📈 Productivity Efficiency Matrix")

st.plotly_chart(
    scatter_plot(
        prod_df,
        x="Outlet_Count",
        y="Total_Sales",
        size="Avg_Sales_Per_Outlet",
        color="Avg_Sales_Per_Outlet",
        title="Sales vs Outlet Coverage Efficiency"
    ),
    use_container_width=True
)

# -------------------------------------------------
# UNDERPERFORMANCE RISK
# -------------------------------------------------
st.markdown("## ⚠ Productivity Risk Zones")

low_productivity = prod_df[
    prod_df["Avg_Sales_Per_Outlet"] < prod_df["Avg_Sales_Per_Outlet"].median()
]

st.dataframe(
    low_productivity.sort_values("Avg_Sales_Per_Outlet"),
    use_container_width=True
)

st.warning(
    "⚠ Field reps with low sales per outlet may require route optimization or incentives."
)

# -------------------------------------------------
# EXECUTIVE INSIGHTS
# -------------------------------------------------
st.markdown("## 🧠 Executive Insights")

st.success(
    """
• High outlet coverage ≠ high productivity  
• Focus on **sales per outlet**, not visit count  
• Data-driven beat optimization can improve ROI by 10–15%
"""
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Field Force Productivity Intelligence • DS Group FMCG Dashboard")
