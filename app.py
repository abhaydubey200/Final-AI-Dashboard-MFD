import streamlit as st
from config import APP_TITLE, APP_TAGLINE
from utils.data_loader import init_session

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    page_icon="📊"
)

# ------------------------------
# Init Session
# ------------------------------
init_session()

# ------------------------------
# Load CSS
# ------------------------------
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------------------
# App Header
# ------------------------------
st.markdown(f"<div class='page-title'>{APP_TITLE}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='page-subtitle'>{APP_TAGLINE}</div>", unsafe_allow_html=True)

# ------------------------------
# Data Status Banner
# ------------------------------
if st.session_state["df"] is None:
    st.warning("📤 No data loaded. Please upload a dataset or connect Snowflake.")
else:
    source = st.session_state["data_source"].upper()
    st.success(f"✅ Data loaded successfully (Source: {source})")
