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
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
)

# -------------------------------------------------
# SIDEBAR UI (MNC LEVEL)
# -------------------------------------------------
with st.sidebar:

    # SAFE LOGO LOAD
    logo_path = "assets/ds_group_logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=180)
    else:
        st.markdown("## 🏢 DS Group")

    st.markdown(f"### {APP_TITLE}")
    st.caption(APP_TAGLINE)

    st.divider()

    # DATA STATUS
    df = st.session_state.get(SESSION_DF_KEY)

    if df is not None:
        st.success("✅ Data Loaded")
        st.caption(f"Source: {st.session_state.get('data_source', 'Unknown')}")
        st.caption(f"Rows: {df.shape[0]:,}")
        st.caption(f"Columns: {df.shape[1]}")
    else:
        st.warning("⚠ No Data Loaded")
        st.caption("Go to **Upload Dataset**")

    st.divider()

    # QUICK ACTIONS
    if st.button("🔄 Reset Application"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.caption("© DS Group | FMCG Executive Intelligence")

# -------------------------------------------------
# MAIN LANDING CONTENT
# -------------------------------------------------
st.markdown(
    f"""
    <div style="padding:20px;border-radius:12px;background:#F5F7FA">
        <h2 style="margin-bottom:5px;">{APP_ICON} {APP_TITLE}</h2>
        <p style="color:#333;">
            {APP_TAGLINE}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### 🚀 How to get started")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        **📤 Upload Dataset**
        - CSV / Excel up to 200MB 
        - Instant analytics  
        - No credentials required
        """
    )

with col2:
    st.markdown(
        """
        **❄️ Snowflake Integration**
        - Secure warehouse access  
        - Auto DB / schema / table  
        - SQL + Explorer support
        """
    )

st.divider()

# -------------------------------------------------
# DATA GUARD (IMPORTANT)
# -------------------------------------------------
if df is None:
    st.info(
        "➡️ Please upload data or connect Snowflake using **Upload Dataset** page.\n\n"
        "Once data is loaded, all dashboards will activate automatically."
    )
else:
    st.success("🎯 Data is ready. Use the sidebar to navigate dashboards.")
