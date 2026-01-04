import streamlit as st
import pandas as pd

from utils.snowflake_connector import get_snowflake_connection
from utils.snowflake_metadata import validate_select_query, execute_query

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(page_title="Snowflake SQL Studio", layout="wide")

st.title("🧠 Snowflake SQL Studio")
st.markdown("Run **read-only SQL queries** securely on Snowflake")

st.divider()

# -------------------------------------------------
# Connection
# -------------------------------------------------
try:
    conn = get_snowflake_connection()
except Exception as e:
    st.error(f"❌ Snowflake connection failed: {e}")
    st.stop()

# -------------------------------------------------
# SQL Editor
# -------------------------------------------------
sql = st.text_area(
    "✍ Write SELECT Query",
    height=200,
    placeholder="SELECT * FROM database.schema.table LIMIT 100;"
)

col1, col2 = st.columns([1, 4])

with col1:
    limit = st.number_input(
        "Row Limit",
        min_value=10,
        max_value=50000,
        value=1000,
        step=100
    )

# -------------------------------------------------
# Execute
# -------------------------------------------------
if st.button("▶ Run Query"):
    try:
        validate_select_query(sql)
        df = execute_query(conn, sql, limit)

        st.success(f"✅ Retrieved {len(df):,} rows")
        st.dataframe(df, use_container_width=True)

        if st.button("➡ Use Result in Dashboard"):
            st.session_state["df"] = df
            st.success("📊 Data loaded into analytics session")

    except Exception as e:
        st.error(f"❌ Query Error: {e}")

# -------------------------------------------------
# Security Note
# -------------------------------------------------
st.info(
    "🔐 Only **SELECT queries** allowed. INSERT / UPDATE / DELETE are blocked."
)
