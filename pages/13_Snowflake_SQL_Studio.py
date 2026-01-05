import streamlit as st
import pandas as pd

st.set_page_config(page_title="Snowflake SQL Studio", layout="wide")

st.title("🧪 Snowflake SQL Studio")

if not st.session_state.get("snowflake_logged"):
    st.warning("🔐 Login via Snowflake Data Ingestion first")
    st.stop()

conn = st.session_state["snowflake_conn"]

query = st.text_area(
    "Write SELECT query only",
    "SELECT * FROM INFORMATION_SCHEMA.TABLES LIMIT 50"
)

if st.button("▶ Run Query"):
    if not query.strip().lower().startswith("select"):
        st.error("❌ Only SELECT queries allowed")
        st.stop()

    try:
        df = pd.read_sql(query, conn)
        df = df.astype(str)  # Arrow-safe
        st.dataframe(df, width="stretch")

    except Exception as e:
        st.error(f"❌ Query failed: {e}")
