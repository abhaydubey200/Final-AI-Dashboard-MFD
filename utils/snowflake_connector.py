# utils/snowflake_connector.py
# --------------------------------------------------
# Snowflake Connection Utility (SAFE)
# --------------------------------------------------

import snowflake.connector
import streamlit as st


def get_snowflake_connection():
    """
    Creates and returns a Snowflake connection using Streamlit secrets.
    """

    if "snowflake" not in st.secrets:
        raise RuntimeError("Snowflake secrets not configured")

    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
    )
