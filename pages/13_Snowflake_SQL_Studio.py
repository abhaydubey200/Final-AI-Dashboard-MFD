import streamlit as st
import pandas as pd
from utils.snowflake_connector import get_snowflake_connection
from config import SESSION_DF_KEY

st.header("🧊 Snowflake SQL Studio")
st.caption("Run secure read-only SQL queries and load results")

# -------------------------------------------------
# GUARD
# -------------------------------------------------
if "snowflake_config" not in st.session_state:
    st.warning("🔐 Login via **Upload Dataset → Snowflake** first")
    st.stop()

conn = get_snowflake_connection()
cur = conn.cursor()

# -------------------------------------------------
# SQL INPUT
# -------------------------------------------------
query = st.text_area(
    "SQL Query (SELECT only)",
    height=180,
    placeholder='SELECT * FROM MY_DB.MY_SCHEMA.MY_TABLE LIMIT 100'
)

# -------------------------------------------------
# EXECUTE
# -------------------------------------------------
if st.button("▶ Run Query"):
    if not query.strip().lower().startswith("select"):
        st.error("❌ Only SELECT queries are allowed")
        st.stop()

    try:
        cur.execute(query)
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description]
        df = pd.DataFrame(rows, columns=cols)

        st.session_state["_sql_result"] = df
        st.success(f"✅ Query executed ({df.shape[0]:,} rows)")
        st.dataframe(df, width="stretch")

    except Exception as e:
        st.error(f"❌ Query failed: {e}")

# -------------------------------------------------
# LOAD INTO APP
# -------------------------------------------------
if "_sql_result" in st.session_state:
    if st.button("📥 Load Result into Application"):
        st.session_state[SESSION_DF_KEY] = st.session_state["_sql_result"]
        st.session_state["data_source"] = "Snowflake SQL"
        st.success("✅ Data loaded into dashboards")
