import streamlit as st
import pandas as pd

from utils.snowflake_connector import get_snowflake_connection
from config import SESSION_DF_KEY

st.header("📤 Data Ingestion")
st.caption("Upload FMCG data or connect to Snowflake")

source = st.radio("Select Data Source", ["Upload File", "Snowflake"])

# =====================================================
# FILE UPLOAD
# =====================================================
if source == "Upload File":
    file = st.file_uploader("Upload CSV / Excel", type=["csv", "xlsx"])

    if file:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.session_state[SESSION_DF_KEY] = df
        st.session_state["data_source"] = "Upload"
        st.success("✅ File uploaded successfully")


# =====================================================
# SNOWFLAKE CONNECTION
# =====================================================
else:
    st.subheader("❄️ Snowflake Connection")

    account = st.text_input("Account")
    user = st.text_input("User")
    password = st.text_input("Password", type="password")
    warehouse = st.text_input("Warehouse")
    database = st.text_input("Database")
    schema = st.text_input("Schema")
    role = st.text_input("Role")

    if st.button("🔌 Connect Snowflake"):
        # ✅ STORE CONFIG (SINGLE SOURCE OF TRUTH)
        st.session_state["snowflake_config"] = {
            "account": account,
            "user": user,
            "password": password,
            "warehouse": warehouse,
            "database": database,
            "schema": schema,
            "role": role,
        }

        try:
            conn = get_snowflake_connection()  # ✅ NO ARGUMENTS
            cur = conn.cursor()
            cur.execute("SELECT CURRENT_VERSION()")
            cur.fetchone()

            st.success("✅ Snowflake connected successfully")
            st.info("➡️ Use Snowflake Explorer or SQL Studio to load data")

        except Exception as e:
            st.error(f"❌ Snowflake connection failed: {e}")
