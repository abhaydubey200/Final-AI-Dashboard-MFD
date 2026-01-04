import streamlit as st
import pandas as pd

from utils.snowflake_connector import get_snowflake_connection
from utils.snowflake_metadata import (
    list_databases,
    list_schemas,
    list_tables,
    fetch_table_sample,
    fetch_table_columns
)

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Snowflake Data Explorer",
    layout="wide"
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("❄️ Snowflake Data Explorer")
st.markdown(
    "Securely browse Snowflake databases, schemas, and tables with live previews."
)

st.divider()

# -------------------------------------------------
# Connect to Snowflake
# -------------------------------------------------
try:
    conn = get_snowflake_connection()
except Exception as e:
    st.error(f"❌ Snowflake connection failed: {e}")
    st.stop()

# -------------------------------------------------
# Database Selector
# -------------------------------------------------
databases = list_databases(conn)

db = st.selectbox(
    "📂 Select Database",
    databases
)

# -------------------------------------------------
# Schema Selector
# -------------------------------------------------
schemas = list_schemas(conn, db)

schema = st.selectbox(
    "🗂 Select Schema",
    schemas
)

# -------------------------------------------------
# Table Selector
# -------------------------------------------------
tables = list_tables(conn, db, schema)

table = st.selectbox(
    "📄 Select Table",
    tables
)

st.divider()

# -------------------------------------------------
# Metadata Section
# -------------------------------------------------
st.subheader("📑 Table Metadata")

col_meta = fetch_table_columns(conn, db, schema, table)

st.dataframe(
    col_meta,
    use_container_width=True
)

# -------------------------------------------------
# Data Preview Section
# -------------------------------------------------
st.subheader("🔍 Data Preview")

row_limit = st.slider(
    "Rows to Preview",
    min_value=10,
    max_value=500,
    value=50,
    step=10
)

sample_df = fetch_table_sample(
    conn,
    db,
    schema,
    table,
    row_limit
)

st.dataframe(
    sample_df,
    use_container_width=True
)

# -------------------------------------------------
# Session Export
# -------------------------------------------------
st.divider()
st.subheader("📥 Load into Analytics Session")

if st.button("➡ Use This Table for Dashboard"):
    st.session_state["df"] = sample_df
    st.success(
        "✅ Table loaded into session. Navigate to analytics pages."
    )

# -------------------------------------------------
# Business Note
# -------------------------------------------------
st.info(
    """
🔐 **Read-Only Mode**
- No updates
- No deletes
- Safe for production Snowflake environments
"""
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Snowflake Explorer • DS Group FMCG Intelligence Platform")
