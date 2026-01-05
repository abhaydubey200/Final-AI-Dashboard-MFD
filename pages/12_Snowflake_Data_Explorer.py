import streamlit as st
import pandas as pd

from utils.schema_normalizer import normalize_dataframe_schema

st.set_page_config(page_title="Snowflake Data Explorer", layout="wide")

st.header("❄️ Snowflake Data Explorer")
st.caption("Browse databases, schemas & tables and load data safely into the application")

# --------------------------------------------------
# Connection check
# --------------------------------------------------
conn = st.session_state.get("snowflake_conn")
if conn is None:
    st.warning("🔐 Login via Snowflake Data Ingestion first")
    st.stop()

# --------------------------------------------------
# Helpers (CORRECT METADATA PARSING)
# --------------------------------------------------
@st.cache_data(show_spinner=False)
def fetch_databases():
    return pd.read_sql("SHOW DATABASES", conn)["name"].tolist()

@st.cache_data(show_spinner=False)
def fetch_schemas(db):
    return pd.read_sql(f'SHOW SCHEMAS IN DATABASE "{db}"', conn)["name"].tolist()

@st.cache_data(show_spinner=False)
def fetch_tables(db, schema):
    return pd.read_sql(
        f'SHOW TABLES IN SCHEMA "{db}"."{schema}"', conn
    )["name"].tolist()

@st.cache_data(show_spinner=False)
def fetch_preview(db, schema, table):
    q = f'SELECT * FROM "{db}"."{schema}"."{table}" LIMIT 200'
    return pd.read_sql(q, conn)

# --------------------------------------------------
# UI
# --------------------------------------------------
db = st.selectbox("Database", fetch_databases())
schema = st.selectbox("Schema", fetch_schemas(db))
table = st.selectbox("Table", fetch_tables(db, schema))

# --------------------------------------------------
# Preview
# --------------------------------------------------
preview_df = fetch_preview(db, schema, table)
st.subheader("🔍 Table Preview (Top 200 Rows)")
st.dataframe(preview_df, width="stretch")

# --------------------------------------------------
# LOAD DATA INTO APPLICATION (FINAL FIX)
# --------------------------------------------------
st.divider()
st.subheader("📥 Load Table into Application")

if st.button("🚀 Load Data & Activate Dashboards"):
    try:
        full_df = pd.read_sql(
            f'SELECT * FROM "{db}"."{schema}"."{table}"',
            conn
        )

        df_final = normalize_dataframe_schema(full_df)

        st.session_state["df"] = df_final
        st.session_state["data_source"] = "snowflake"
        st.session_state["active_table"] = f"{db}.{schema}.{table}"

        st.success("✅ Data loaded successfully. All dashboards are now active.")

    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
