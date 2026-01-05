import streamlit as st
import pandas as pd

from utils.snowflake_connector import get_snowflake_connection

st.header("❄️ Snowflake Data Explorer")
st.caption("Browse databases, schemas & tables safely")

conn = st.session_state.get("snowflake_conn")

if conn is None:
    st.warning("🔐 Login via Snowflake Data Ingestion first")
    st.stop()


@st.cache_data(show_spinner=False)
def fetch_list(query):
    return pd.read_sql(query, conn).iloc[:, 0].dropna().tolist()


# -------------------------------
# DATABASE
# -------------------------------
databases = fetch_list("SHOW DATABASES")
db = st.selectbox("Database", databases)

st.session_state["sf_database"] = db

# -------------------------------
# SCHEMA
# -------------------------------
schemas = fetch_list(f'SHOW SCHEMAS IN DATABASE "{db}"')
schema = st.selectbox("Schema", schemas)

st.session_state["sf_schema"] = schema

# -------------------------------
# TABLE
# -------------------------------
tables = fetch_list(f'SHOW TABLES IN SCHEMA "{db}"."{schema}"')
table = st.selectbox("Table", tables)

st.session_state["sf_table"] = table

st.success(f"Selected: {db}.{schema}.{table}")

# -------------------------------
# PREVIEW
# -------------------------------
if st.button("👁 Preview Table"):
    q = f'SELECT * FROM "{db}"."{schema}"."{table}" LIMIT 200'
    df = pd.read_sql(q, conn)
    st.dataframe(df, width="stretch")

    st.session_state["preview_df"] = df

# -------------------------------
# LOAD DATA
# -------------------------------
if st.button("📥 Load Data into Dashboard"):
    if "preview_df" not in st.session_state:
        st.warning("Preview table first")
    else:
        st.session_state["df"] = st.session_state["preview_df"]
        st.session_state["data_source"] = "Snowflake Explorer"
        st.success("✅ Data loaded into application")
        st.rerun()
