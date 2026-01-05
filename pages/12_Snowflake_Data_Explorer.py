import streamlit as st
import pandas as pd

from utils.snowflake_connector import get_snowflake_connection
from config import SESSION_DF_KEY

st.header("❄️ Snowflake Data Explorer")
st.caption("Browse databases, schemas & tables and load data into the application")

conn = get_snowflake_connection()
if conn is None:
    st.warning("🔐 Connect Snowflake from **Upload Dataset** page first")
    st.stop()


@st.cache_data(show_spinner=False)
def fetch_list(query):
    cur = conn.cursor()
    cur.execute(query)
    return [r[0] for r in cur.fetchall() if r[0] is not None]


@st.cache_data(show_spinner=False)
def fetch_preview(db, schema, table):
    q = f'SELECT * FROM "{db}"."{schema}"."{table}" LIMIT 500'
    return pd.read_sql(q, conn)


# ------------------ UI ------------------

dbs = fetch_list("SHOW DATABASES")
db = st.selectbox("Database", dbs)

schemas = fetch_list(f'SHOW SCHEMAS IN DATABASE "{db}"')
schema = st.selectbox("Schema", schemas)

tables = fetch_list(f'SHOW TABLES IN SCHEMA "{db}"."{schema}"')
table = st.selectbox("Table", tables)

if st.button("👁 Preview Data"):
    df_preview = fetch_preview(db, schema, table)
    st.dataframe(df_preview, width="stretch")

    if st.button("📥 Load data into application"):
        st.session_state[SESSION_DF_KEY] = df_preview
        st.session_state["data_source"] = "Snowflake"
        st.success("✅ Data loaded successfully into application")
