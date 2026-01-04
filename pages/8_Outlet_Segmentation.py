import streamlit as st
import plotly.express as px
import pandas as pd

from config import SESSION_DF_KEY
from utils.segmentation import (
    prepare_outlet_features,
    segment_outlets
)
from utils.column_detector import auto_detect_columns

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Outlet Segmentation",
    layout="wide"
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Upload dataset or connect Snowflake first.")
    st.stop()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("🏪 Outlet Segmentation & Risk Profiling")
st.markdown(
    "AI-driven outlet clustering to optimize **distribution strategy, schemes, "
    "credit policy, and field-force focus**."
)

st.divider()

# -------------------------------------------------
# Segmentation Controls
# -------------------------------------------------
with st.expander("⚙ Segmentation Configuration", expanded=True):

    clusters = st.slider(
        "Number of Outlet Segments",
        min_value=2,
        max_value=6,
        value=3
    )

# -------------------------------------------------
# Prepare Outlet Features
# -------------------------------------------------
outlet_df = prepare_outlet_features(df)

if outlet_df.empty:
    st.error("❌ Unable to prepare outlet-level features.")
    st.stop()

# -------------------------------------------------
# Apply Segmentation
# -------------------------------------------------
segmented_df = segment_outlets(outlet_df, n_clusters=clusters)

# -------------------------------------------------
# Risk Scoring (NEW – Executive Requirement)
# -------------------------------------------------
if "Total_Sales" in segmented_df.columns:
    segmented_df["Risk_Score"] = pd.qcut(
        segmented_df["Total_Sales"],
        q=3,
        labels=["High Risk", "Medium Risk", "Low Risk"]
    )
else:
    segmented_df["Risk_Score"] = "Unknown"

# -------------------------------------------------
# KPIs
# -------------------------------------------------
st.markdown("## 📌 Segmentation KPIs")

k1, k2, k3 = st.columns(3)

k1.metric(
    "Total Outlets",
    segmented_df.shape[0]
)

k2.metric(
    "High Value Outlets",
    (segmented_df["Segment_Label"] == "High Value").sum()
)

k3.metric(
    "High Risk Outlets",
    (segmented_df["Risk_Score"] == "High Risk").sum()
)

st.divider()

# -------------------------------------------------
# Segmented Table
# -------------------------------------------------
st.markdown("## 📋 Outlet Segmentation Table")

st.dataframe(
    segmented_df.sort_values(
        by="Total_Sales" if "Total_Sales" in segmented_df.columns else segmented_df.columns[0],
        ascending=False
    ),
    use_container_width=True
)

# -------------------------------------------------
# Visualization
# -------------------------------------------------
numeric_cols = segmented_df.select_dtypes(include="number").columns.tolist()

if len(numeric_cols) >= 2:
    st.markdown("## 📊 Outlet Cluster Visualization")

    fig = px.scatter(
        segmented_df,
        x=numeric_cols[0],
        y=numeric_cols[1],
        color="Segment_Label",
        symbol="Risk_Score",
        hover_data=[segmented_df.columns[0]],
        title="Outlet Segments with Risk Overlay"
    )

    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Segment Summary
# -------------------------------------------------
st.markdown("## 📈 Segment Performance Summary")

summary = (
    segmented_df
    .groupby("Segment_Label")[numeric_cols]
    .mean()
    .round(2)
    .reset_index()
)

st.dataframe(summary, use_container_width=True)

# -------------------------------------------------
# Executive Insight
# -------------------------------------------------
st.success(
    """
🧠 **Executive Insight**

• Focus schemes & credit on **High Value / Medium Risk** outlets  
• Deploy field-force aggressively on **High Risk outlets**  
• Rationalize effort on consistently **Low Value outlets**

This segmentation directly improves **ROI per outlet**.
"""
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Outlet Intelligence Engine • DS Group FMCG Analytics Platform")
