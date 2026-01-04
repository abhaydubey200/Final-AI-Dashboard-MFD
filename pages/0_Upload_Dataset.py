# -------------------------------------------------
# Page 0 : Upload Dataset / Snowflake Connector
# -------------------------------------------------

import streamlit as st
import pandas as pd

from config import SESSION_DF_KEY

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📤",
    layout="wide"
)

st.title("📤 Data Ingestion")
st.caption("Upload FMCG sales data or connect to Snowflake")

st.divider()

# -------------------------------------------------
# Source Selector
# -------------------------------------------------
source = st.radio(
    "Select Data Source",
    ["Upload File", "Snowflake"],
    horizontal=True
)

# -------------------------------------------------
# FILE UPLOAD MODE
# -------------------------------------------------
if source == "Upload File":
    uploaded_file = st.file_uploader(
        "Upload CSV / Excel File",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            if df.empty:
                st.error("Uploaded file is empty.")
            else:
                st.session_state[SESSION_DF_KEY] = df
                st.session_state["data"] = df
                st.session_state["source"] = "upload"

                st.success("✅ File uploaded successfully")
                st.write("### Preview")
                st.dataframe(df.head(50), use_container_width=True)

        except Exception as e:
            st.error("Failed to read uploaded file")
            st.exception(e)

# -------------------------------------------------
# SNOWFLAKE MODE (PLACEHOLDER – SAFE)
# -------------------------------------------------
else:
    st.info(
        "❄️ Snowflake integration is enabled at architecture level.\n\n"
        "Connection UI & query execution will be activated "
        "once credentials are configured."
    )

    with st.expander("Snowflake Connection (Preview)", expanded=False):
        st.text_input("Account")
        st.text_input("User")
        st.text_input("Warehouse")
        st.text_input("Database")
        st.text_input("Schema")
        st.text_input("Role")
        st.text_input("Password", type="password")

        st.button("Connect (Disabled)", disabled=True)

# -------------------------------------------------
# Footer Status
# -------------------------------------------------
st.divider()

if st.session_state.get(SESSION_DF_KEY) is not None:
    st.success(
        f"Dataset Active | Rows: {len(st.session_state[SESSION_DF_KEY]):,}"
    )
else:
    st.warning("No dataset loaded yet.")
