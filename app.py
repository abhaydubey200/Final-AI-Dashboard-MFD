import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="DS Group FMCG AI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# SESSION STATE INITIALIZATION (CRITICAL)
# --------------------------------------------------
if "df" not in st.session_state:
    st.session_state["df"] = None

if "data_source" not in st.session_state:
    st.session_state["data_source"] = None

if "snowflake_conn" not in st.session_state:
    st.session_state["snowflake_conn"] = None

# --------------------------------------------------
# SIDEBAR – BRANDING & STATUS
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center">
            <h2 style="color:#1F7A4F;">DS GROUP</h2>
            <p><b>FMCG AI Intelligence Platform</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Data status
    if st.session_state["df"] is not None:
        st.success("✅ Data Loaded")
        st.caption(f"Source: {st.session_state.get('data_source', 'Unknown')}")
        st.caption(f"Rows: {len(st.session_state['df']):,}")
    else:
        st.warning("⚠ No data loaded")

    st.divider()

    st.caption("📌 Use sidebar navigation to explore dashboards")

# --------------------------------------------------
# MAIN LANDING UI
# --------------------------------------------------
st.markdown(
    """
    <h1 style="margin-bottom:0;">📊 FMCG Business Intelligence</h1>
    <p style="color:gray; margin-top:4px;">
        AI-powered analytics for Sales, Distribution, Pricing & Forecasting
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()

# --------------------------------------------------
# QUICK ACTION CARDS
# --------------------------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        ### 📤 Upload Data
        Upload FMCG sales files (CSV / Excel) and instantly activate dashboards.
        """
    )
    if st.button("Go to Upload Page ➜"):
        st.switch_page("pages/0_Upload_Dataset.py")

with c2:
    st.markdown(
        """
        ### ❄️ Snowflake
        Connect enterprise Snowflake warehouse and analyze data securely.
        """
    )
    if st.button("Go to Snowflake Explorer ➜"):
        st.switch_page("pages/12_Snowflake_Data_Explorer.py")

with c3:
    st.markdown(
        """
        ### 🧠 AI Analytics
        Forecast demand, segment outlets, optimize pricing & performance.
        """
    )
    if st.button("Open Executive Overview ➜"):
        st.switch_page("pages/1_Executive_Overview.py")

st.divider()

# --------------------------------------------------
# DATA PREVIEW (IF LOADED)
# --------------------------------------------------
if st.session_state["df"] is not None:
    st.subheader("🔍 Active Dataset Preview")

    st.dataframe(
        st.session_state["df"].head(100),
        width="stretch"
    )

    st.caption(
        "This dataset is now shared across all dashboards."
    )

else:
    st.info(
        "ℹ️ Load data using **Upload Dataset** or **Snowflake** to activate analytics."
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <hr>
    <div style="text-align:center; color:gray;">
        DS Group • AI FMCG Analytics Platform<br>
        Built for enterprise-grade decision making
    </div>
    """,
    unsafe_allow_html=True,
)
