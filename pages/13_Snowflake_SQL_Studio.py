import streamlit as st
import pandas as pd

from utils.snowflake_connector import get_snowflake_connection
from utils.snowflake_context import get_snowflake_context, is_snowflake_context_ready

st.header("❄️ Snowflake SQL Studio")
st.caption("Run secure read-only queries and load data into application")

# --------------------------------------------------
# CONNECTION CHECK
# --------------------------------------------------
conn = st.session_state.get("snowflake_conn")

if conn is None:
    st.warning("🔐 Login via Snowflake Data Ingestion first")
    st.stop()

# --------------------------------------------------
# CONTEXT CHECK (CRITICAL FIX)
# --------------------------------------------------
db, schema, table = get_snowflake_context()

if not is_snowflake_context_ready():
    st.warning("⚠️ Select Database → Schema → Table in Snowflake Data Explorer")
    st.stop()

st.success(f"Context: `{db}.{schema}.{table}`")

# --------------------------------------------------
# SQL EDITOR
# --------------------------------------------------
default_query = f'''
SELECT *
FROM "{db}"."{schema}"."{table}"
LIMIT 200
'''

query = st.text_area(
    "SQL Query (READ ONLY)",
    value=default_query,
    height=180
)

# --------------------------------------------------
# RUN QUERY
# --------------------------------------------------
if st.button("▶ Run Query"):
    try:
        df = pd.read_sql(query, conn)
        st.dataframe(df, width="stretch")

        st.session_state["preview_df"] = df
        st.success(f"Fetched {len(df)} rows")

    except Exception as e:
        st.error("❌ Query failed")
        st.exception(e)

# --------------------------------------------------
# LOAD DATA INTO APPLICATION
# --------------------------------------------------
if st.button("📥 Load Data into Dashboard"):
    if "preview_df" not in st.session_state:
        st.warning("Run query first")
    else:
        st.session_state["df"] = st.session_state["preview_df"]
        st.session_state["data_source"] = "Snowflake SQL Studio"
        st.success("✅ Data loaded into application")
        st.rerun()
