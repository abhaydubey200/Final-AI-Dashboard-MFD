import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Snowflake SQL Studio",
    layout="wide"
)

st.header("🧠 Snowflake SQL Studio")
st.caption("Run secure read-only SQL queries on Snowflake")

# --------------------------------------------------
# Validate Snowflake Login
# --------------------------------------------------
if not st.session_state.get("snowflake_logged"):
    st.warning("🔐 Login via **Snowflake Data Ingestion** first")
    st.stop()

conn = st.session_state.get("snowflake_conn")

if conn is None:
    st.error("❌ Snowflake connection not found in session")
    st.stop()

# --------------------------------------------------
# SQL Input
# --------------------------------------------------
st.subheader("📝 SQL Editor (Read-Only)")

query = st.text_area(
    "Enter SQL Query",
    height=180,
    placeholder="SELECT * FROM MFD_DWH.MFD_SCHEMA.SALES_FACT LIMIT 100"
)

# --------------------------------------------------
# Query Validation (Security)
# --------------------------------------------------
def is_safe_select(query: str) -> bool:
    query = query.strip().lower()
    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate", "merge"]
    return query.startswith("select") and not any(word in query for word in forbidden)

# --------------------------------------------------
# Execute Query
# --------------------------------------------------
if st.button("▶ Run Query"):
    if not query.strip():
        st.warning("⚠️ Please enter a SQL query")
        st.stop()

    if not is_safe_select(query):
        st.error("🚫 Only SELECT queries are allowed")
        st.stop()

    try:
        with st.spinner("Executing query on Snowflake..."):
            df = pd.read_sql(query, conn)

        st.success(f"✅ Query executed successfully ({len(df)} rows)")

        # Fix Arrow issues
        df = df.astype(str)

        st.dataframe(
            df,
            width="stretch",
            height=420
        )

    except Exception as e:
        st.error("❌ Query execution failed")
        st.exception(e)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption("❄️ Snowflake SQL Studio • Read-Only Enterprise Console")
