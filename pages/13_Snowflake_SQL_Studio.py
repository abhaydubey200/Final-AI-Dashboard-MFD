import streamlit as st
import pandas as pd

from utils.snowflake_connector import get_snowflake_connection
from utils.schema_normalizer import normalize_dataframe_schema

st.set_page_config(page_title="Snowflake SQL Studio", layout="wide")

st.header("❄️ Snowflake SQL Studio")
st.caption("Run secure read-only SQL queries and load data into the application")

# --------------------------------------------------
# Connection check
# --------------------------------------------------
conn = st.session_state.get("snowflake_conn")

if conn is None:
    st.warning("🔐 Login via Snowflake Data Ingestion first")
    st.stop()

# --------------------------------------------------
# SQL Editor
# --------------------------------------------------
query = st.text_area(
    "Write SELECT query only",
    height=180,
    placeholder="SELECT * FROM MFD_DWH.MFD_SCHEMA.SALES_FACT LIMIT 100"
)

run_query = st.button("▶ Run Query")

df_result = None

if run_query:
    if not query.strip().lower().startswith("select"):
        st.error("❌ Only SELECT queries are allowed")
    else:
        try:
            df_result = pd.read_sql(query, conn)
            st.success(f"✅ Query executed successfully ({len(df_result)} rows)")
        except Exception as e:
            st.error(f"❌ Query execution failed: {e}")

# --------------------------------------------------
# Preview
# --------------------------------------------------
if df_result is not None and not df_result.empty:
    st.subheader("🔍 Query Result Preview")
    st.dataframe(df_result, width="stretch")

# --------------------------------------------------
# LOAD DATA INTO APPLICATION (CRITICAL FIX)
# --------------------------------------------------
if df_result is not None and not df_result.empty:
    if st.button("📥 Load Data into Application"):
        try:
            df_final = normalize_dataframe_schema(df_result)

            st.session_state["df"] = df_final
            st.session_state["data_source"] = "snowflake"
            st.session_state["schema_normalized"] = True

            st.success("✅ Data loaded successfully. All dashboards are now active.")

        except Exception as e:
            st.error(f"❌ Failed to load data into application: {e}")
