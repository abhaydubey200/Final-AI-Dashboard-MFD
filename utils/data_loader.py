import pandas as pd
import streamlit as st
from config import SESSION_DF_KEY, SESSION_SOURCE_KEY


def load_dataset(file):
    try:
        if file.name.lower().endswith(".csv"):
            df = pd.read_csv(file, encoding="latin1")
        elif file.name.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file format")
            return None

        if df.empty:
            st.error("Uploaded file is empty")
            return None

        st.session_state[SESSION_DF_KEY] = df
        st.session_state[SESSION_SOURCE_KEY] = "uploader"

        return df

    except Exception as e:
        st.error(f"Upload failed: {e}")
        return None
