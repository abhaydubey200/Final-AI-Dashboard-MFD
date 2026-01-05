import streamlit as st
import pandas as pd

st.set_page_config(page_title="Snowflake Data Explorer", layout="wide")

st.title("🧊 Snowflake Data Explorer")

if not st.session_state.get("snowflake_logged"):
    st.warning("🔐 Login via Snowflake Data Ingestion first")
    st.stop()

conn = st.session_state["snowflake_conn"]
cur = conn.cursor()

# ---------------- DATABASES ----------------
cur.execute("SHOW DATABASES")
dbs = [r[1] for r in cur.fetchall()]
database = st.selectbox("Database", dbs)

# ---------------- SCHEMAS ----------------
cur.execute(f"SHOW SCHEMAS IN DATABASE {database}")
schemas = [r[1] for r in cur.fetchall()]
schema = st.selectbox("Schema", schemas)

# ---------------- TABLES ----------------
cur.execute(f"SHOW TABLES IN {database}.{schema}")
tables = [r[1] for r in cur.fetchall()]
table = st.selectbox("Table", tables)

# ---------------- PREVIEW ----------------
if st.button("🔍 Preview Data"):
    query = f'SELECT * FROM "{database}"."{schema}"."{table}" LIMIT 100'
    df = pd.read_sql(query, conn)

    df = df.astype(str)  # 🔥 Arrow-safe
    st.dataframe(df, width="stretch")
