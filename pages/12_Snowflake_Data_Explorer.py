# --------------------------------------------------
#  Snowflake Data Explorer 
# --------------------------------------------------

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Snowflake Explorer", layout="wide")

st.header("❄️ Snowflake Data Explorer")
st.caption(
    "Explore enterprise Snowflake data securely. "
    "This integration is optional and will not break the app."
)

# --------------------------------------------------
# Enable / Disable Snowflake
# --------------------------------------------------
use_snowflake = st.toggle("Enable Snowflake Integration", value=False)

if not use_snowflake:
    st.info(
        "Snowflake is disabled.\n\n"
        "Turn this ON only if credentials and connector are configured."
    )
    st.stop()

# --------------------------------------------------
# SAFE IMPORT (NO CRASH EVER)
# --------------------------------------------------
try:
    from utils.snowflake_connector import get_snowflake_connection
except Exception:
    st.error(
        "Snowflake connector not found.\n\n"
        "Missing file: utils/snowflake_connector.py"
    )
    st.stop()

# --------------------------------------------------
# CONNECT
# --------------------------------------------------
try:
    conn = get_snowflake_connection()
    st.success("Connected to Snowflake")
except Exception as e:
    st.error("Snowflake connection failed")
    st.exception(e)
    st.stop()

# --------------------------------------------------
# QUERY UI
# --------------------------------------------------
st.subheader("🧠 SQL Query Editor")

query = st.text_area(
    "Write SQL Query",
    value="SELECT CURRENT_DATABASE(), CURRENT_SCHEMA();",
    height=160
)

run = st.button("▶ Run Query")

if run:
    try:
        df = pd.read_sql(query, conn)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error("Query execution error")
        st.exception(e)

st.caption(
    "Tip: Limit rows for large tables to avoid performance issues."
)
