import streamlit as st
import pandas as pd

from utils.snowflake_connector import get_snowflake_connection
from config import SESSION_DF_KEY

st.header("🧊 Snowflake SQL Studio")
st.caption("Run secure read-only SQL queries and load results into dashboards")

conn = get_snowflake_connection()
if conn is None:
    st.warning("🔐 Connect Snowflake from **Upload Dataset** page first")
    st.stop()


query = st.text_area(
    "SQL Query (SELECT only)",
    height=180,
    placeholder='SELECT * FROM DATABASE.SCHEMA.TABLE LIMIT 100'
)

if st.button("▶ Run Query"):
    try:
        df = pd.read_sql(query, conn)
        st.dataframe(df, width="stretch")

        if st.button("📥 Load result into application"):
            st.session_state[SESSION_DF_KEY] = df
            st.session_state["data_source"] = "Snowflake"
            st.success("✅ Query result loaded into application")

    except Exception as e:
        st.error(f"❌ Query failed: {e}")
