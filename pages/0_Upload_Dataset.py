import streamlit as st
import pandas as pd
from utils.snowflake_connector import get_snowflake_connection

st.set_page_config(page_title="Data Ingestion", layout="wide")

st.title("📤 Data Ingestion")
st.caption("Upload FMCG data or connect to Snowflake")

# ---------------- SESSION INIT ----------------
st.session_state.setdefault("df", None)
st.session_state.setdefault("snowflake_logged", False)
st.session_state.setdefault("snowflake_conn", None)

source = st.radio("Select Data Source", ["Upload File", "Snowflake"], horizontal=True)

# ---------------- FILE UPLOAD ----------------
if source == "Upload File":
    file = st.file_uploader("Upload CSV / Excel", type=["csv", "xlsx"])

    if file:
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
        st.session_state["df"] = df
        st.success("✅ File uploaded successfully")

# ---------------- SNOWFLAKE LOGIN ----------------
else:
    st.subheader("❄️ Snowflake Connection")

    with st.form("snowflake_login"):
        account = st.text_input("Account")
        user = st.text_input("User")
        password = st.text_input("Password", type="password")
        warehouse = st.text_input("Warehouse")
        database = st.text_input("Database")
        schema = st.text_input("Schema")
        role = st.text_input("Role")

        login = st.form_submit_button("🔐 Login")

    if login:
        try:
            conn = get_snowflake_connection(
                account, user, password, warehouse, database, schema, role
            )
            st.session_state["snowflake_conn"] = conn
            st.session_state["snowflake_logged"] = True
            st.success("✅ Snowflake connected successfully")

        except Exception as e:
            st.error(f"❌ Snowflake connection failed: {e}")
