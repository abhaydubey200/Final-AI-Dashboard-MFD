import streamlit as st
import pandas as pd

from utils.snowflake_connector import get_snowflake_connection
from utils.snowflake_metadata import validate_select_query, execute_query

st.set_page_config(page_title="Snowflake SQL Studio", layout="wide")
st.header("🧊 Snowflake SQL Studio")

creds = st.session_state.get("snowflake_creds")

if not creds:
    st.warning("Login via Snowflake Data Ingestion first")
    st.stop()

query = st.text_area(
    "Write SELECT query",
    height=200,
    placeholder="SELECT * FROM YOUR_TABLE LIMIT 100"
)

if st.button("Run Query"):
    if not validate_select_query(query):
        st.error("❌ Only SELECT queries are allowed")
        st.stop()

    try:
        conn = get_snowflake_connection(creds)
        cur = execute_query(conn, query)
        df = pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description])

        st.dataframe(df, use_container_width=True)
        st.success("✅ Query executed successfully")

    except Exception as e:
        st.error(f"❌ Query failed: {e}")
