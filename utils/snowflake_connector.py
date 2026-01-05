# --------------------------------------------------
# ❄️ Snowflake Connector Utility
# --------------------------------------------------

import streamlit as st
import snowflake.connector

def get_snowflake_connection():
    """
    Create and return Snowflake connection using Streamlit secrets
    """

    try:
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"],
            role=st.secrets["snowflake"]["role"],
        )
        return conn

    except Exception as e:
        raise RuntimeError(f"Snowflake connection error: {e}")
