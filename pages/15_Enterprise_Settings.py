import streamlit as st
from config import (
    DEBUG_MODE,
    MAX_FORECAST_MONTHS,
    MAX_CLUSTERS
)

st.set_page_config(page_title="Enterprise Settings", layout="wide")

st.title("🏢 Enterprise Governance & Settings")
st.markdown("Platform configuration & execution boundaries")

st.divider()

# -------------------------------------------------
# Environment
# -------------------------------------------------
st.subheader("🌍 Environment")

env = "Production" if not DEBUG_MODE else "Development"

st.info(f"**Current Environment:** {env}")

# -------------------------------------------------
# Forecasting Limits
# -------------------------------------------------
st.subheader("📈 Forecasting Limits")

st.metric("Max Forecast Horizon (Months)", MAX_FORECAST_MONTHS)
st.metric("Max Segmentation Clusters", MAX_CLUSTERS)

# -------------------------------------------------
# Session Info
# -------------------------------------------------
st.subheader("🧠 Session State")

st.json(list(st.session_state.keys()))

# -------------------------------------------------
# Reset Controls
# -------------------------------------------------
st.divider()

if st.button("🧹 Clear Session & Reset App"):
    st.session_state.clear()
    st.success("✅ Session cleared. Reload application.")

# -------------------------------------------------
# Compliance Note
# -------------------------------------------------
st.info(
    """
🔐 Governance Rules:
- Snowflake access is READ-ONLY
- Session data is memory-based
- No persistent storage without approval
"""
)
