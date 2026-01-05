# --------------------------------------------------
# ❄️ Snowflake SQL Studio (Production Ready)
# --------------------------------------------------

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Snowflake SQL Studio",
    layout="wide"
)

st.header("❄️ Snowflake SQL Studio")
st.caption(
    "Enterprise-grade SQL workspace for Snowflake\n"
    "Read-only | Secure | Production-safe"
)

# --------------------------------------------------
# Enable Snowflake
# --------------------------------------------------
enable_snowflake = st.toggle(
    "Enable Snowflake SQL Studio",
    value=False
)

if not enable_snowflake:
    st.info("Enable Snowflake only when credentials are configured.")
    st.stop()

# --------------------------------------------------
# SAFE IMPORT
# --------------------------------------------------
try:
    from utils.snowflake_connector import get_snowflake_connection
except Exception:
    st.error(
        "Snowflake connector missing.\n\n"
        "Required file: utils/snowflake_connector.py"
    )
    st.stop()

# --------------------------------------------------
# SAFE SQL VALIDATION (INLINE)
# --------------------------------------------------
def validate_select_query(query: str) -> bool:
    if not query:
        return False
    q = query.strip().lower()
    return q.startswith("select")

# --------------------------------------------------
# CONNECT TO SNOWFLAKE
# --------------------------------------------------
try:
    conn = get_snowflake_connection()
    st.success("Connected to Snowflake")
except Exception as e:
    st.error("Failed to connect to Snowflake")
    st.exception(e)
    st.stop()

# --------------------------------------------------
# SQL EDITOR
# --------------------------------------------------
st.subheader("🧠 SQL Editor")

query = st.text_area(
    "Write SELECT query only",
    height=180,
    value="SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE();"
)

run_query = st.button("▶ Run Query")

# --------------------------------------------------
# EXECUTION
# --------------------------------------------------
if run_query:
    if not validate_select_query(query):
        st.error("Only SELECT queries are allowed")
        st.stop()

    try:
        df = pd.read_sql(query, conn)

        if df.empty:
            st.warning("Query executed successfully but returned no data")
        else:
            st.success(f"Returned {len(df):,} rows")
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error("Query execution failed")
        st.exception(e)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.caption("Snowflake SQL Studio • Read-only • Production Safe")
