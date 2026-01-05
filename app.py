import streamlit as st
import os
import pandas as pd

from config import (
    APP_TITLE,
    APP_TAGLINE,
    SESSION_DF_KEY,
)

# -------------------------------------------------
# PAGE CONFIG (DS GROUP BRANDING)
# -------------------------------------------------
st.set_page_config(
    page_title="Home | DS Group FMCG AI",
    page_icon="assets/ds_group_favicon.png",
    layout="wide",
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

# -------------------------------------------------
# SIDEBAR (ENTERPRISE NAV)
# -------------------------------------------------
with st.sidebar:

    if os.path.exists("assets/ds_group_logo.png"):
        st.image("assets/ds_group_logo.png", width=160)
    else:
        st.markdown("## 🏢 DS Group")

    st.markdown("### 🏠 Home")
    st.caption("FMCG Executive Intelligence Platform")

    st.divider()

    if df is not None:
        st.success("✅ Data Connected")
        st.markdown(
            f"""
            **Source:** `{st.session_state.get("data_source", "Uploaded / Snowflake")}`  
            **Records:** `{df.shape[0]:,}`  
            **Metrics:** `{df.shape[1]}`
            """
        )
    else:
        st.warning("⚠ No Active Dataset")

    st.divider()

    if st.button("🔄 Reset Application", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.caption("© DS Group | Confidential")

# -------------------------------------------------
# HEADER (EXECUTIVE HERO)
# -------------------------------------------------
st.markdown(
    """
    <div style="
        padding:30px;
        border-radius:18px;
        background:linear-gradient(135deg,#FFFFFF,#F4F6F9);
        border:1px solid #E3E6EB;
        margin-bottom:25px;">
        <h1 style="margin-bottom:6px;">📊 DS Group FMCG AI Command Center</h1>
        <p style="font-size:16px;color:#333;">
            Enterprise-grade analytics, forecasting & AI decision intelligence
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# EXECUTIVE KPI TILES
# -------------------------------------------------
st.markdown("## 📌 Executive Snapshot")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

if df is not None:
    kpi1.metric("Total Records", f"{df.shape[0]:,}")
    kpi2.metric("Total Variables", df.shape[1])
    kpi3.metric("Data Freshness", "Latest")
    kpi4.metric("AI Readiness", "High 🚀")
else:
    kpi1.metric("Total Records", "—")
    kpi2.metric("Total Variables", "—")
    kpi3.metric("Data Freshness", "—")
    kpi4.metric("AI Readiness", "—")

# -------------------------------------------------
# AI CEO SUMMARY PREVIEW
# -------------------------------------------------
st.markdown("## 🧠 AI CEO Summary")

if df is None:
    st.info(
        "Upload FMCG data or connect Snowflake to generate an **AI-powered CEO summary**."
    )
else:
    st.markdown(
        """
        <div style="
            padding:24px;
            border-radius:16px;
            background:#FFFFFF;
            border:1px solid #E0E0E0;
            line-height:1.7;
            ">
            <h4>📈 Executive Intelligence Brief</h4>
            <p>
            Based on the ingested FMCG dataset, the AI identifies 
            <b>key sales drivers, outlet performance variance, and demand volatility trends</b>.
            </p>
            <p>
            Preliminary insights indicate opportunities in 
            <b>distribution optimization, inventory rationalization, and region-wise demand forecasting</b>.
            </p>
            <p>
            Leadership teams can leverage AI modules to:
            </p>
            <ul>
                <li>🔍 Identify underperforming outlets</li>
                <li>📦 Optimize stock allocation</li>
                <li>🔮 Forecast category-level demand</li>
                <li>⚠ Detect churn & risk signals early</li>
            </ul>
            <p style="color:#555;">
            👉 Navigate to dashboards & AI Analyst for deep-dive insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------------------------
# NEXT STEPS
# -------------------------------------------------
st.markdown("## 🚀 Next Actions")

c1, c2, c3 = st.columns(3)

c1.info("📤 Upload / Refresh FMCG Dataset")
c2.info("📊 Explore Executive Dashboards")
c3.info("🤖 Ask AI Analyst Strategic Questions")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(
    """
    <div style="margin-top:50px;text-align:center;color:#777;font-size:13px;">
        DS Group FMCG AI Platform • Secure • Scalable • Boardroom Ready
    </div>
    """,
    unsafe_allow_html=True,
)
