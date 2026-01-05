# pages/8_Outlet_Segmentation.py
# --------------------------------------------------
# 🏪 Outlet Segmentation & Risk Profiling (PRODUCTION)
# --------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.column_detector import auto_detect_columns
from utils.segmentation import segment_outlets

st.header("🏪 Outlet Segmentation & Risk Profiling")
st.caption(
    "AI-driven outlet clustering to optimize distribution strategy, schemes, credit policy, and field-force focus."
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("Please upload a dataset first.")
    st.stop()

# --------------------------------------------------
# Auto Detect Columns
# --------------------------------------------------
cols = auto_detect_columns(df)

outlet_col = cols.get("outlet")
sales_col = cols.get("sales")
qty_col = cols.get("quantity")
date_col = cols.get("date")

if not outlet_col:
    st.error("Outlet column not detected in dataset.")
    st.stop()

# --------------------------------------------------
# Feature Engineering (SAFE)
# --------------------------------------------------
features = df.copy()

if date_col:
    features[date_col] = pd.to_datetime(features[date_col], errors="coerce")

agg_map = {}

if sales_col:
    agg_map[sales_col] = "sum"
if qty_col:
    agg_map[qty_col] = "sum"
if date_col:
    agg_map[date_col] = "max"

outlet_df = (
    features.groupby(outlet_col)
    .agg(agg_map)
    .reset_index()
)

# Rename for consistency
rename_map = {}
if sales_col:
    rename_map[sales_col] = "Total_Sales"
if qty_col:
    rename_map[qty_col] = "Total_Quantity"
if date_col:
    rename_map[date_col] = "Last_Order_Date"

outlet_df.rename(columns=rename_map, inplace=True)

# --------------------------------------------------
# Risk Scoring (NEW – EXECUTIVE GRADE)
# --------------------------------------------------
if "Last_Order_Date" in outlet_df.columns:
    outlet_df["Days_Since_Last_Order"] = (
        pd.Timestamp.today() - outlet_df["Last_Order_Date"]
    ).dt.days

    outlet_df["Risk_Score"] = pd.cut(
        outlet_df["Days_Since_Last_Order"],
        bins=[-1, 30, 60, 9999],
        labels=["Low Risk", "Medium Risk", "High Risk"]
    )
else:
    outlet_df["Risk_Score"] = "Unknown"

# --------------------------------------------------
# Segmentation Controls
# --------------------------------------------------
st.subheader("⚙ Segmentation Configuration")

clusters = st.slider(
    "Number of Outlet Segments",
    min_value=2,
    max_value=6,
    value=3
)

# --------------------------------------------------
# Apply Segmentation
# --------------------------------------------------
try:
    segmented_df = segment_outlets(outlet_df, clusters)
except Exception as e:
    st.error("Segmentation failed due to insufficient numeric features.")
    st.exception(e)
    st.stop()

# --------------------------------------------------
# KPI Summary
# --------------------------------------------------
st.subheader("📊 Segment KPIs")

k1, k2, k3 = st.columns(3)

k1.metric("Total Outlets", segmented_df.shape[0])
k2.metric("High Risk Outlets", (segmented_df["Risk_Score"] == "High Risk").sum())
k3.metric("Total Sales", f"₹ {segmented_df.get('Total_Sales', pd.Series()).sum():,.0f}")

# --------------------------------------------------
# Segmentation Visualization
# --------------------------------------------------
num_cols = segmented_df.select_dtypes("number").columns.tolist()

if len(num_cols) >= 2:
    fig = px.scatter(
        segmented_df,
        x=num_cols[0],
        y=num_cols[1],
        color="Segment",
        hover_data=[outlet_col, "Risk_Score"],
        title="Outlet Clusters"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Segmented Table
# --------------------------------------------------
st.subheader("📋 Outlet Segmentation Table")

st.dataframe(segmented_df, use_container_width=True)

# --------------------------------------------------
# Business Insight
# --------------------------------------------------
st.success(
    "Outlet segmentation and risk profiling completed successfully. "
    "Use High-Risk outlets for credit tightening and Medium-Risk for scheme optimization."
)
