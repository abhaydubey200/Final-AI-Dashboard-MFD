import streamlit as st
import pandas as pd
from utils.snowflake_connector import get_snowflake_connection
from config import SESSION_DF_KEY

st.header("❄️ Snowflake Data Explorer")
st.caption("Browse databases, schemas & tables and load data safely")

# -------------------------------------------------
# GUARD
# -------------------------------------------------
if "snowflake_config" not in st.session_state:
    st.warning("🔐 Login via **Upload Dataset → Snowflake** first")
    st.stop()

conn = get_snowflake_connection()
cur = conn.cursor()

# -------------------------------------------------
# HELPERS (NO CACHE)
# -------------------------------------------------
def list_first_column(sql):
    cur.execute(sql)
    return [row[0] for row in cur.fetchall() if row[0]]

def fetch_table_preview(db, schema, table, limit=500):
    sql = f'SELECT * FROM "{db}"."{schema}"."{table}" LIMIT {limit}'
    cur.execute(sql)
    rows = cur.fetchall()
    cols = [c[0] for c in cur.description]
    return pd.DataFrame(rows, columns=cols)

# -------------------------------------------------
# UI FLOW
# -------------------------------------------------
databases = list_first_column("SHOW DATABASES")
db = st.selectbox("Database", databases)

schemas = list_first_column(f'SHOW SCHEMAS IN DATABASE "{db}"')
schema = st.selectbox("Schema", schemas)

tables = list_first_column(f'SHOW TABLES IN SCHEMA "{db}"."{schema}"')
table = st.selectbox("Table", tables)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
if st.button("📥 Load Data into Application"):
    try:
        df = fetch_table_preview(db, schema, table)
        st.session_state[SESSION_DF_KEY] = df
        st.session_state["data_source"] = f"Snowflake: {db}.{schema}.{table}"
        st.success(f"✅ Loaded {df.shape[0]:,} rows")
        st.dataframe(df, width="stretch")
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
