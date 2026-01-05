import snowflake.connector
import streamlit as st

@st.cache_resource(show_spinner=False)
def get_snowflake_connection():
    cfg = st.session_state.get("snowflake_config")
    if not cfg:
        return None

    return snowflake.connector.connect(
        account=cfg["account"],
        user=cfg["user"],
        password=cfg["password"],
        warehouse=cfg["warehouse"],
        database=cfg["database"],
        schema=cfg["schema"],
        role=cfg["role"],
    )
