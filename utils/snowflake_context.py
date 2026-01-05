import streamlit as st

REQUIRED_KEYS = ["sf_database", "sf_schema", "sf_table"]

def is_snowflake_context_ready() -> bool:
    return all(st.session_state.get(k) for k in REQUIRED_KEYS)


def get_snowflake_context():
    if not is_snowflake_context_ready():
        return None, None, None

    return (
        st.session_state["sf_database"],
        st.session_state["sf_schema"],
        st.session_state["sf_table"],
    )
