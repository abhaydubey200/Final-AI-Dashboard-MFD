# pages/6_Pricing_Discount_Analysis.py
# --------------------------------------------------
# 💸 Pricing & Discount Analysis (PRODUCTION SAFE)
# --------------------------------------------------

import streamlit as st
import pandas as pd

from utils.column_detector import auto_detect_columns
from utils.visualizations import bar_top

st.header("💸 Pricing & Discount Analysis")
st.caption("Analyze discount impact on sales & pricing effectiveness")

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("Please upload a dataset first.")
    st.stop()

# --------------------------------------------------
# Auto Detect Columns (OLD LOGIC)
# --------------------------------------------------
cols = auto_detect_columns(df)

sales_col = cols.get("sales")
qty_col = cols.get("quantity")
discount_col = cols.get("discount")
brand_col = cols.get("brand")

# --------------------------------------------------
# Derived Price (SAFE)
# --------------------------------------------------
df = df.copy()

if sales_col and qty_col:
    df["__unit_price__"] = df[sales_col] / df[qty_col].replace(0, pd.NA)
else:
    df["__unit_price__"] = None

# --------------------------------------------------
# Pricing Distribution
# --------------------------------------------------
st.subheader("🏷 Pricing Distribution")

if df["__unit_price__"].notna().any():
    st.line_chart(
        df["__unit_price__"].dropna(),
        use_container_width=True
    )
else:
    st.info("Unit price cannot be derived from available columns.")

# --------------------------------------------------
# Discount Impact
# --------------------------------------------------
st.subheader("📉 Discount Impact on Sales")

if discount_col and sales_col:
    try:
        st.plotly_chart(
            bar_top(
                df,
                discount_col,
                sales_col,
                "Sales by Discount Level"
            ),
            use_container_width=True
        )
    except Exception:
        st.info("Unable to visualize discount impact.")
else:
    st.info("Discount column not detected.")

# --------------------------------------------------
# Brand-wise Pricing
# --------------------------------------------------
st.subheader("🏷 Brand-wise Average Price")

if brand_col and df["__unit_price__"].notna().any():
    try:
        avg_price = (
            df.groupby(brand_col)["__unit_price__"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        st.bar_chart(
            avg_price.set_index(brand_col),
            use_container_width=True
        )
    except Exception:
        st.info("Unable to compute brand pricing.")
else:
    st.info("Brand or pricing data not available.")

# --------------------------------------------------
# Success
# --------------------------------------------------
st.success("Pricing & Discount Analysis loaded successfully ✅")
