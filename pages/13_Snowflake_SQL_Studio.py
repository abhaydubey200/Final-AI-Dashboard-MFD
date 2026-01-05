import streamlit as st
import pandas as pd

from utils.schema_normalizer import normalize_dataframe_schema
from utils.snowflake_metadata import validate_select_query

st.set_page_config(page_title="Snowflake SQL Studio", layout="wide")

st.header("🧠 Snowflake SQL Studio")
st.caption("Run secure read-only SQL queries and load results into dashboards")

# --------------------------------------------------
# Connection check
# --------------------------------------------------
conn = st.session_state.get("snowflake_conn")
if conn is None:
    st.warning("🔐 Login via Snowflake Data Ingestion first")
    st.stop()

# --------------------------------------------------
# SQL Input
# --------------------------------------------------
sql = st.text_area(
    "Enter SELECT query",
    height=180,
    placeholder='SELECT * FROM MFD_DWH.MFD_SCHEMA.SALES LIMIT 1000'
)

# --------------------------------------------------
# Run Query
# --------------------------------------------------
if st.button("▶ Run Query"):
    if not validate_select_query(sql):
        st.error("❌ Only SELECT queries are allowed")
        st.stop()

    try:
        result_df = pd.read_sql(sql, conn)
        st.session_state["sql_result_df"] = result_df

        st.subheader("📊 Query Result Preview")
        st.dataframe(result_df, width="stretch")

    except Exception as e:
        st.error(f"❌ Query failed: {e}")
        st.stop()

# --------------------------------------------------
# LOAD QUERY RESULT INTO APPLICATION (FINAL FIX)
# --------------------------------------------------
if "sql_result_df" in st.session_state:
    st.divider()
    st.subheader("📥 Load Query Result into Application")

    if st.button("🚀 Load Data & Activate Dashboards"):
        try:
            df_final = normalize_dataframe_schema(
                st.session_state["sql_result_df"]
            )

            st.session_state["df"] = df_final
            st.session_state["data_source"] = "snowflake_sql"

            st.success("✅ Query result loaded successfully")

        except Exception as e:
            st.error(f"❌ Failed to load data: {e}")
