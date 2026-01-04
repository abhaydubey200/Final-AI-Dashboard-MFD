import pandas as pd
import streamlit as st

# ------------------------------
# Session Initializer
# ------------------------------
def init_session():
    defaults = {
        "df": None,
        "data_source": "upload",
        "snowflake_connected": False,
        "snowflake_meta": {}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ------------------------------
# File Upload Loader
# ------------------------------
def load_uploaded_file(file):
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file, engine="openpyxl")

        st.session_state["df"] = df
        st.session_state["data_source"] = "upload"
        return df

    except Exception as e:
        st.error(f"❌ Upload failed: {e}")
        return None


# ------------------------------
# Snowflake Loader (placeholder)
# ------------------------------
def load_from_snowflake(df):
    """
    df already fetched from Snowflake connector
    """
    st.session_state["df"] = df
    st.session_state["data_source"] = "snowflake"
    st.session_state["snowflake_connected"] = True
