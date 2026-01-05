import streamlit as st
import pandas as pd

from utils.snowflake_connector import get_snowflake_connection
from utils.schema_normalizer import normalize_dataframe_schema

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Snowflake SQL Studio",
    layout="wide"
)

st.header("❄️ Snowflake SQL Studio")
st.caption("Run secure read-only SQL queries and load data into the application")

# -------------------------------------------------
# Connection check
# -------------------------------------------------
conn = st.session_state.get("snowflake_conn")

if conn is None:
    st.warning("🔐 Login via Snowflake Data Ingestion first")
    st.stop()

# -------------------------------------------------
# Init session state
# -------------------------------------------------
if "snowflake_query_df" not in st.session_state:
    st.session_state["snowflake_query_df"] = None

# -------------------------------------------------
# SQL Editor
# -------------------------------------------------
query = st.text_area(
    "Write SELECT query only",
    height=180,
    placeholder="SELECT * FROM MFD_DWH.MFD_SCHEMA.SALES_FACT LIMIT 100"
)

col_run, col_clear = st.columns([1, 1])

with col_run:
    run_query = st.button("▶ Run Query")

with col_clear:
    clear_data = st.button("🧹 Clear Result")

if clear_data:
    st.session_state["snowflake_query_df"] = None
    st.info("Query result cleared")

# -------------------------------------------------
# Execute Query
# -------------------------------------------------
if run_query:
    if not query.strip().lower().startswith("select"):
        st.error("❌ Only SELECT queries are allowed")
    else:
        try:
            df = pd.read_sql(query, conn)

            if df.empty:
                st.warning("Query executed but returned no rows")
            else:
                st.session_state["snowflake_query_df"] = df
                st.success(f"✅ Query executed successfully ({len(df)} rows)")

        except Exception as e:
            st.error(f"❌ Query execution failed: {e}")

# -------------------------------------------------
# Preview Section
# -------------------------------------------------
df_result = st.session_state.get("snowflake_query_df")

if df_result is not None and not df_result.empty:
    st.subheader("🔍 Query Result Preview")
    st.dataframe(df_result, width="stretch")

# -------------------------------------------------
# LOAD DATA INTO APPLICATION (FINAL FIX)
# -------------------------------------------------
if df_result is not None and not df_result.empty:
    st.divider()

    st.subheader("📥 Load Data into Application")

    if st.button("🚀 Load Data & Activate Dashboards"):
        try:
            df_final = normalize_dataframe_schema(df_result)

            st.session_state["df"] = df_final
            st.session_state["data_source"] = "snowflake"
            st.session_state["schema_normalized"] = True

            st.success("✅ Data loaded successfully. All dashboards are now active.")

        except Exception as e:
            st.error(f"❌ Failed to load data into application: {e}")
