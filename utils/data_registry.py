import streamlit as st
import pandas as pd

SESSION_DF_KEY = "MFD_LOADED_DATAFRAME"


def set_loaded_dataframe(df: pd.DataFrame):
    """Register dataframe globally in session state"""
    st.session_state[SESSION_DF_KEY] = df


def get_loaded_dataframe() -> pd.DataFrame | None:
    """Safely fetch dataframe from session state"""
    return st.session_state.get(SESSION_DF_KEY)
