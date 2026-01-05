import streamlit as st
import os

from config import (
    APP_TITLE,
    APP_TAGLINE,
    APP_ICON,
    LAYOUT,
    SESSION_DF_KEY,
)

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title=f"Home | {APP_TITLE}",
    page_icon=APP_ICON,
    layout=LAYOUT,
)

# -------------------------------------------------
# SIDEBAR (ENTERPRISE UI)
# -------------------------------------------------
with st.sidebar:

    # LOGO
    logo_path = "assets/ds_group_logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=170)
    else:
        st.markdown("## 🏢 DS Group")

    st.markdown("## 🏠 Home")
    st.caption("Executive Control Center")

    st.divider()

    # DATA STATUS CARD
    df = st.session_state.get(SESSION_DF_KEY)

    if df is not None:
        st.success("✅ Data Connected")
        st.markdown(
            f"""
            **Source:** `{st.session_state.get("data_source", "Unknown")}`  
            **Rows:** `{df.shape[0]:,}`  
            **Columns:** `{df.shape[1]}`
            """
        )
    else:
        st.warning("⚠ No Data Connected")
        st.caption("Use **Upload Dataset** to begin")

    st.divider()

    # QUICK ACTIONS
    st.markdown("### ⚙ Quick Actions")

    if st.button("🔄 Reset Application", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.divider()
    st.caption("© DS Group | FMCG Executive Intelligence Platform")

# -------------------------------------------------
# MAIN HOME UI
# -------------------------------------------------
st.markdown(
    f"""
    <div style="
        padding:28px;
        border-radius:16px;
        background:linear-gradient(135deg,#F5F7FA,#FFFFFF);
        border:1px solid #E0E0E0;
        ">
        <h1 style="margin-bottom:4px;">{APP_ICON} {APP_TITLE}</h1>
        <p style="font-size:16px;color:#333;">
            {APP_TAGLINE}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")

# -------------------------------------------------
# EXECUTIVE INTRO
# -------------------------------------------------
st.markdown("## 🎯 Executive Overview")
st.markdown(
    """
This platform delivers **production-grade FMCG intelligence** by combining:

- 📊 Advanced sales & distribution analytics  
- 🔮 AI-driven forecasting & segmentation  
- ❄️ Secure Snowflake warehouse integration  
- 🧠 Actionable insights for CXOs & leadership  

Designed for **speed, scale, and decision confidence**.
"""
)

st.divider()

# -------------------------------------------------
# GETTING STARTED
# -------------------------------------------------
st.markdown("## 🚀 Get Started in 2 Steps")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        ### 📤 Upload Dataset
        - CSV / Excel upload  
        - Instant validation  
        - No credentials required  

        👉 Best for quick analysis
        """
    )

with col2:
    st.markdown(
        """
        ### ❄️ Connect Snowflake
        - Secure warehouse access  
        - SQL-based ingestion  
        - Enterprise-grade governance  

        👉 Best for production data
        """
    )

st.divider()

# -------------------------------------------------
# DATA GUARD
# -------------------------------------------------
if df is None:
    st.info(
        "➡️ **No data detected.**\n\n"
        "Please upload a dataset or connect Snowflake using **Upload Dataset**.\n\n"
        "Once data is available, all dashboards will activate automatically."
    )
else:
    st.success(
        "🎯 **Data Ready!**\n\n"
        "Navigate using the sidebar to explore dashboards, forecasts, and AI insights."
    )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(
    """
    <div style="margin-top:40px;text-align:center;color:#777;font-size:13px;">
        Built for enterprise FMCG analytics • Secure • Scalable • AI-powered
    </div>
    """,
    unsafe_allow_html=True,
)
