import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Snowflake Data Explorer",
    layout="wide"
)

st.header("❄️ Snowflake Data Explorer")

# --------------------------------------------------
# Validate Snowflake session
# --------------------------------------------------
df = st.session_state.get("df")
source = st.session_state.get("data_source")

if df is None or source != "snowflake":
    st.warning("❗ Please load data from Snowflake first using Data Ingestion page")
    st.stop()

# --------------------------------------------------
# Fix Arrow serialization issues (CRITICAL)
# --------------------------------------------------
def make_arrow_safe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert mixed-type columns to string to avoid Arrow crashes.
    Production-safe for Snowflake data.
    """
    safe_df = df.copy()

    for col in safe_df.columns:
        # Object columns often break Arrow
        if safe_df[col].dtype == "object":
            safe_df[col] = safe_df[col].astype(str)

    # Replace common Snowflake null strings
    safe_df.replace(
        ["None", "nan", "NaN", "NULL"],
        np.nan,
        inplace=True
    )

    return safe_df


safe_df = make_arrow_safe(df)

# --------------------------------------------------
# Dataset Overview
# --------------------------------------------------
st.subheader("📄 Dataset Overview")

st.dataframe(
    safe_df,
    width="stretch",
    height=420
)

# --------------------------------------------------
# Metadata Summary
# --------------------------------------------------
st.subheader("📊 Column Summary")

summary_df = pd.DataFrame({
    "Column": safe_df.columns,
    "Data Type": safe_df.dtypes.astype(str),
    "Non-Null Count": safe_df.notnull().sum().values
})

st.dataframe(
    summary_df,
    width="stretch",
    height=300
)

# --------------------------------------------------
# Basic Stats (Numeric Only)
# --------------------------------------------------
numeric_cols = safe_df.select_dtypes(include=["int", "float"]).columns

if len(numeric_cols) > 0:
    st.subheader("📈 Numeric Statistics")
    st.dataframe(
        safe_df[numeric_cols].describe().T,
        width="stretch"
    )
else:
    st.info("ℹ️ No numeric columns available for statistical summary")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption("❄️ Powered by Snowflake • Enterprise Data Explorer")
