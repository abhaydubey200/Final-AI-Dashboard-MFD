# -------------------------------------------------
# DS Group – FMCG Executive Intelligence Dashboard
# Main App Entry (Production Ready)
# -------------------------------------------------

import os
import streamlit as st

from config import (
    APP_TITLE,
    APP_TAGLINE,
    APP_ICON,
    LAYOUT,
    SESSION_DF_KEY
)

# -------------------------------------------------
# Page Configuration (GLOBAL)
# -------------------------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Sidebar Branding (SAFE FOR CLOUD)
# -------------------------------------------------
LOGO_PATH = os.path.join(os.getcwd(), "assets", "ds_group_logo.png")

with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    else:
        st.markdown(
            """
            <h3 style="margin-bottom:0">DS Group</h3>
            <p style="font-size:12px;color:#666">
                FMCG Executive Intelligence
            </p>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.markdown(
        f"""
        <b>{APP_TITLE}</b><br>
        <span style="font-size:12px;color:#666">
            {APP_TAGLINE}
        </span>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# Session State Initialization (CRITICAL)
# -------------------------------------------------
if SESSION_DF_KEY not in st.session_state:
    st.session_state[SESSION_DF_KEY] = None

if "data" not in st.session_state:
    st.session_state["data"] = None

if "source" not in st.session_state:
    st.session_state["source"] = None  # upload | snowflake

# -------------------------------------------------
# Main Landing UI
# -------------------------------------------------
st.markdown(
    """
    <style>
        .hero-title {
            font-size: 34px;
            font-weight: 800;
            color: #000;
        }
        .hero-subtitle {
            font-size: 16px;
            color: #555;
            margin-bottom: 20px;
        }
        .hero-card {
            background: #ffffff;
            padding: 22px;
            border-radius: 18px;
            border: 1px solid #e6e6e6;
            box-shadow: 0 8px 22px rgba(0,0,0,0.06);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="hero-title">{APP_ICON} {APP_TITLE}</div>
    <div class="hero-subtitle">{APP_TAGLINE}</div>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------
# App Status Section
# -------------------------------------------------
st.markdown('<div class="hero-card">', unsafe_allow_html=True)

if st.session_state.get(SESSION_DF_KEY) is None:
    st.warning(
        "📤 **No dataset loaded yet.**\n\n"
        "Please start with **Upload Dataset** or connect via **Snowflake** "
        "from the left sidebar to activate analytics pages."
    )
else:
    st.success(
        f"✅ **Dataset Loaded Successfully**\n\n"
        f"Source: **{st.session_state.get('source', 'Unknown')}**\n\n"
        f"Rows: **{len(st.session_state[SESSION_DF_KEY]):,}**"
    )

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Navigation Help
# -------------------------------------------------
st.markdown(
    """
    ### 🧭 How to Use This Platform

    **Step 1️⃣** Upload data or connect Snowflake  
    **Step 2️⃣** Explore KPI & Sales Dashboards  
    **Step 3️⃣** Analyze Outlets, Warehouses & Pricing  
    **Step 4️⃣** Use AI Forecasting & Actionable Insights  

    👉 Use the **left sidebar** to navigate across modules.
    """
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown(
    """
    <hr>
    <div style="text-align:center;font-size:12px;color:#777;">
        © DS Group • FMCG Executive Intelligence Platform<br>
        Built for enterprise-scale decision making
    </div>
    """,
    unsafe_allow_html=True
)
