import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Snowflake Data Explorer",
    layout="wide"
)

st.header("❄️ Snowflake Data Explorer")
st.caption("Browse databases, schemas & tables safely")

# --------------------------------------------------
# Validate Snowflake Login
# --------------------------------------------------
if not st.session_state.get("snowflake_logged"):
    st.warning("🔐 Login via Snowflake Data Ingestion first")
    st.stop()

conn = st.session_state.get("snowflake_conn")
if conn is None:
    st.error("❌ Snowflake connection missing")
    st.stop()

# --------------------------------------------------
# Load Metadata
# --------------------------------------------------
@st.cache_data(show_spinner=False)
def load_tables():
    return pd.read_sql(
        """
        SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        """,
        conn
    )

tables_df = load_tables()

# --------------------------------------------------
# UI – Table Selector
# --------------------------------------------------
st.subheader("📦 Select Table")

db = st.selectbox(
    "Database",
    sorted(tables_df["TABLE_CATALOG"].unique())
)

schema = st.selectbox(
    "Schema",
    sorted(tables_df[tables_df["TABLE_CATALOG"] == db]["TABLE_SCHEMA"].unique())
)

table = st.selectbox(
    "Table",
    sorted(
        tables_df[
            (tables_df["TABLE_CATALOG"] == db) &
            (tables_df["TABLE_SCHEMA"] == schema)
        ]["TABLE_NAME"].unique()
    )
)

# --------------------------------------------------
# Fetch Data
# --------------------------------------------------
if st.button("📥 Load Table Data"):
    try:
        query = f'SELECT * FROM "{db}"."{schema}"."{table}" LIMIT 1000'
        df = pd.read_sql(query, conn)

        # Arrow safety
        df = df.astype(str)

        st.session_state["df"] = df

        st.success(f"✅ Loaded {len(df)} rows from {table}")

        st.dataframe(
            df,
            width="stretch",
            height=450
        )

    except Exception as e:
        st.error("❌ Failed to load table")
        st.exception(e)
