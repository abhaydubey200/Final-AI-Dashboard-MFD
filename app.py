import streamlit as st
from config import (
    APP_TITLE,
    APP_TAGLINE,
    APP_ICON,
    LAYOUT,
    SESSION_DF_KEY
)

# -------------------------------------------------
# GLOBAL PAGE CONFIG (ONLY HERE)
# -------------------------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# GLOBAL CSS (ENTERPRISE UI)
# -------------------------------------------------
st.markdown(
    """
    <style>
        /* App background */
        .stApp {
            background-color: #f7f9fb;
        }

        /* Sidebar branding */
        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e6e6e6;
        }

        /* Remove Streamlit default padding */
        .block-container {
            padding-top: 1.5rem;
        }

        /* KPI font consistency */
        div[data-testid="metric-container"] {
            background: #ffffff;
            border-radius: 14px;
            padding: 16px;
            border: 1px solid #e6e6e6;
            box-shadow: 0 6px 18px rgba(0,0,0,0.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# SIDEBAR — BRANDING
# -------------------------------------------------
with st.sidebar:
    st.image("assets/ds_group_logo.png", use_container_width=True)
    st.markdown(
        f"""
        <div style="font-size:18px;font-weight:800;margin-top:10px;">
            {APP_TITLE}
        </div>
        <div style="font-size:13px;color:#666;margin-bottom:12px;">
            {APP_TAGLINE}
        </div>
        """,
        unsafe_allow_html=True
    )
    st.divider()

# -------------------------------------------------
# SESSION STATE INITIALIZATION (SINGLE SOURCE)
# -------------------------------------------------
if SESSION_DF_KEY not in st.session_state:
    st.session_state[SESSION_DF_KEY] = None

if "DATA_SOURCE" not in st.session_state:
    st.session_state["DATA_SOURCE"] = None  # UPLOAD / SNOWFLAKE

if "SNOWFLAKE_CONNECTED" not in st.session_state:
    st.session_state["SNOWFLAKE_CONNECTED"] = False

# -------------------------------------------------
# SIDEBAR — DATA STATUS
# -------------------------------------------------
with st.sidebar:
    st.markdown("### 📦 Data Status")

    if st.session_state[SESSION_DF_KEY] is not None:
        st.success("✅ Dataset Loaded")
        st.caption(f"Source: {st.session_state.get('DATA_SOURCE')}")
        st.caption(f"Rows: {len(st.session_state[SESSION_DF_KEY]):,}")
    else:
        st.warning("❌ No Dataset Loaded")

    st.divider()

# -------------------------------------------------
# SIDEBAR — GOVERNANCE
# -------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡 Governance")

    st.caption("• Read-only Snowflake")
    st.caption("• Session-based memory")
    st.caption("• No auto persistence")

# -------------------------------------------------
# ROUTING NOTE
# -------------------------------------------------
st.markdown(
    """
    <div style="
        background:#ffffff;
        padding:18px;
        border-radius:16px;
        border:1px solid #e6e6e6;
        box-shadow:0 6px 18px rgba(0,0,0,0.05);
    ">
        <h3>👋 Welcome to DS Group Executive Intelligence Platform</h3>
        <p>
            This enterprise-grade FMCG analytics system supports:
        </p>
        <ul>
            <li>📤 Excel & Snowflake data ingestion</li>
            <li>📊 Executive dashboards</li>
            <li>🔮 AI forecasting & segmentation</li>
            <li>🧠 CEO-level insights</li>
            <li>🛡 Governance & data quality controls</li>
        </ul>
        <p style="margin-top:10px;">
            👉 Use the <b>left navigation menu</b> to begin.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(
    """
    <hr>
    <div style="text-align:center;font-size:12px;color:#777;">
        DS Group FMCG Executive Intelligence Platform • Production Deployment
    </div>
    """,
    unsafe_allow_html=True
)
