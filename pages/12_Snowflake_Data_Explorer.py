import streamlit as st
import pandas as pd

from utils.snowflake_connector import get_snowflake_connection
from utils.schema_normalizer import normalize_dataframe_schema

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Snowflake Data Explorer",
    layout="wide"
)

st.header("❄️ Snowflake Data Explorer")
st.caption("Browse databases, schemas & tables and load data safely into the application")

# -------------------------------------------------
# Connection check
# -------------------------------------------------
conn = st.session_state.get("snowflake_conn")

if conn is None:
    st.warning("🔐 Login via Snowflake Data Ingestion first")
    st.stop()

# -------------------------------------------------
# Helpers
# -------------------------------------------------
@st.cache_data(show_spinner=False)
def fetch_list(query):
    return pd.read_sql(query, conn).iloc[:, 0].tolist()

@st.cache_data(show_spinner=False)
def fetch_table_preview(db, schema, table, limit=200):
    q = f'SELECT * FROM "{db}"."{schema}"."{table}" LIMIT {limit}'
    return pd.read_sql(q, conn)

# -------------------------------------------------
# Step 1: Database
# -------------------------------------------------
databases = fetch_list("SHOW DATABASES")

db = st.selectbox("Database", databases)

# -------------------------------------------------
# Step 2: Schema
# -------------------------------------------------
schemas = fetch_list(f'SHOW SCHEMAS IN DATABASE "{db}"')
schema = st.selectbox("Schema", schemas)

# -------------------------------------------------
# Step 3: Table
# -------------------------------------------------
tables = fetch_list(f'SHOW TABLES IN SCHEMA "{db}"."{schema}"')
table = st.selectbox("Table", tables)

# -------------------------------------------------
# Preview Table
# -------------------------------------------------
if table:
    try:
        preview_df = fetch_table_preview(db, schema, table)

        st.subheader("🔍 Table Preview (Top 200 Rows)")
        st.dataframe(preview_df, width="stretch")

    except Exception as e:
        st.error(f"❌ Failed to load table preview: {e}")
        st.stop()

# -------------------------------------------------
# LOAD DATA INTO APPLICATION (NEW BUTTON ✅)
# -------------------------------------------------
if table and not preview_df.empty:
    st.divider()
    st.subheader("📥 Load Table into Application")

    if st.button("🚀 Load Data & Activate Dashboards"):
        try:
            full_query = f'SELECT * FROM "{db}"."{schema}"."{table}"'
            full_df = pd.read_sql(full_query, conn)

            df_final = normalize_dataframe_schema(full_df)

            st.session_state["df"] = df_final
            st.session_state["data_source"] = "snowflake"
            st.session_state["active_table"] = f"{db}.{schema}.{table}"
            st.session_state["schema_normalized"] = True

            st.success(
                f"✅ `{db}.{schema}.{table}` loaded successfully. "
                "All dashboards are now active."
            )

        except Exception as e:
            st.error(f"❌ Failed to load data into application: {e}")
