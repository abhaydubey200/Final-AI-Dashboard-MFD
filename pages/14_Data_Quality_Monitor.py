import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Data Quality Monitor", layout="wide")

st.title("🧪 Enterprise Data Quality Monitor")
st.markdown("Automated data health checks for leadership confidence")

st.divider()

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = st.session_state.get("df")

if df is None:
    st.warning("📤 No dataset loaded")
    st.stop()

# -------------------------------------------------
# Metrics
# -------------------------------------------------
total_rows = len(df)
total_cols = df.shape[1]
null_cells = df.isna().sum().sum()
duplicate_rows = df.duplicated().sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Rows", f"{total_rows:,}")
c2.metric("Columns", total_cols)
c3.metric("Null Values", f"{null_cells:,}")
c4.metric("Duplicate Rows", f"{duplicate_rows:,}")

st.divider()

# -------------------------------------------------
# Null Analysis
# -------------------------------------------------
st.subheader("🚨 Column-wise Null Analysis")

null_df = (
    df.isna().sum()
    .reset_index()
    .rename(columns={"index": "Column", 0: "Null_Count"})
)

null_df["Null_%"] = (null_df["Null_Count"] / total_rows * 100).round(2)

st.dataframe(
    null_df.sort_values("Null_%", ascending=False),
    use_container_width=True
)

# -------------------------------------------------
# Freshness Check
# -------------------------------------------------
date_cols = df.select_dtypes(include=["datetime", "object"]).columns

st.subheader("⏱ Data Freshness")

freshness_results = []

for col in date_cols:
    try:
        parsed = pd.to_datetime(df[col], errors="coerce")
        freshness_results.append({
            "Column": col,
            "Latest_Date": parsed.max(),
            "Oldest_Date": parsed.min()
        })
    except:
        pass

if freshness_results:
    st.dataframe(pd.DataFrame(freshness_results), use_container_width=True)

# -------------------------------------------------
# Verdict
# -------------------------------------------------
st.success("✅ Data quality checks completed successfully")
