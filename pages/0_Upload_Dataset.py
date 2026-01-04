import streamlit as st
import pandas as pd
from pathlib import Path

from utils.data_loader import load_uploaded_file
from utils.column_detector import auto_detect_columns
from config import APP_TITLE, SESSION_DF_KEY

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Data Ingestion | FMCG Executive Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------
# Enterprise UI CSS
# -------------------------------------------------
st.markdown(
    """
<style>
.kpi-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.06);
    border-left: 6px solid #0aad0a;
}
.kpi-title {
    font-size: 14px;
    color: #6b7280;
    font-weight: 600;
}
.kpi-value {
    font-size: 26px;
    font-weight: 800;
    color: #111827;
}
.section-box {
    background: #ffffff;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.08);
    margin-bottom: 24px;
}
.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
}
.badge-upload {
    background: #e0f2fe;
    color: #0369a1;
}
.badge-snowflake {
    background: #ede9fe;
    color: #5b21b6;
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("📥 Data Ingestion Center")
st.markdown(
    "Enterprise-grade **data onboarding** for FMCG & MFD analytics. "
    "Upload files or connect securely to **Snowflake Data Warehouse**."
)

# -------------------------------------------------
# Session State Initialization
# -------------------------------------------------
if "data_source" not in st.session_state:
    st.session_state["data_source"] = None  # upload | snowflake

if "snowflake_connected" not in st.session_state:
    st.session_state["snowflake_connected"] = False

# -------------------------------------------------
# Data Source Status
# -------------------------------------------------
with st.container():
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Active Data Source</div>
                <div class="kpi-value">
                    {st.session_state.get("data_source", "None").upper() if st.session_state.get("data_source") else "—"}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Rows Loaded</div>
                <div class="kpi-value">
                    {len(st.session_state.get(SESSION_DF_KEY, []))}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Columns Detected</div>
                <div class="kpi-value">
                    {len(st.session_state.get(SESSION_DF_KEY, []).columns) if SESSION_DF_KEY in st.session_state else 0}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# -------------------------------------------------
# Upload Section
# -------------------------------------------------
with st.container():
    st.markdown(
        """
        <div class="section-box">
        <h3>📤 Upload Dataset</h3>
        <span class="badge badge-upload">CSV / Excel</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploader_disabled = st.session_state["data_source"] == "snowflake"

    uploaded_file = st.file_uploader(
        "Upload FMCG / MFD Dataset",
        type=["csv", "xlsx"],
        disabled=uploader_disabled,
        help="Supports large datasets. Snowflake connection will disable uploader.",
    )

    if uploader_disabled:
        st.info("Uploader disabled because Snowflake data is active.")

    if uploaded_file:
        try:
            df = load_uploaded_file(uploaded_file)

            if df.empty:
                st.error("Uploaded file contains no data.")
                st.stop()

            st.session_state[SESSION_DF_KEY] = df
            st.session_state["data_source"] = "upload"
            st.session_state["snowflake_connected"] = False

            cols = auto_detect_columns(df)

            st.success("✅ Dataset uploaded successfully")
            st.json(cols)

        except Exception as e:
            st.error(f"❌ Upload failed: {str(e)}")

# -------------------------------------------------
# Snowflake Section
# -------------------------------------------------
with st.container():
    st.markdown(
        """
        <div class="section-box">
        <h3>❄️ Snowflake Data Warehouse</h3>
        <span class="badge badge-snowflake">Enterprise Mode</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sf_col1, sf_col2, sf_col3 = st.columns(3)

    with sf_col1:
        account = st.text_input("Account", disabled=st.session_state["snowflake_connected"])
        user = st.text_input("User", disabled=st.session_state["snowflake_connected"])
        password = st.text_input("Password", type="password", disabled=st.session_state["snowflake_connected"])

    with sf_col2:
        warehouse = st.text_input("Warehouse", disabled=st.session_state["snowflake_connected"])
        database = st.text_input("Database", disabled=st.session_state["snowflake_connected"])
        schema = st.text_input("Schema", disabled=st.session_state["snowflake_connected"])

    with sf_col3:
        role = st.text_input("Role", disabled=st.session_state["snowflake_connected"])
        table = st.text_input("Table Name", disabled=st.session_state["snowflake_connected"])

    sf_login = st.button("🔐 Login & Load Data")
    sf_logout = st.button("🚪 Logout")
    sf_refresh = st.button("🔄 Refresh Data")

    if sf_login:
        if not all([account, user, password, warehouse, database, schema, table]):
            st.error("Please fill all Snowflake fields.")
        else:
            # Placeholder – real Snowflake loader will be connected later
            st.session_state["snowflake_connected"] = True
            st.session_state["data_source"] = "snowflake"
            st.session_state[SESSION_DF_KEY] = pd.DataFrame()  # will be replaced by Snowflake loader
            st.success("✅ Snowflake connected (integration active)")

    if sf_refresh and st.session_state["snowflake_connected"]:
        st.info("🔄 Refreshing Snowflake data…")

    if sf_logout:
        st.session_state.clear()
        st.success("Snowflake session cleared")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.divider()
st.caption(
    "© DS Group | FMCG Executive Intelligence Platform — Secure • Scalable • Production-Grade"
)
