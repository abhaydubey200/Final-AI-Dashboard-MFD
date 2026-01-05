import streamlit as st
import pandas as pd

from utils.snowflake_connector import (
    get_snowflake_connection,
    fetch_table_df
)

st.set_page_config(page_title="Data Ingestion", layout="wide")
st.header("📤 Data Ingestion")

source = st.radio(
    "Select Data Source",
    ["Upload File", "Snowflake"],
    horizontal=True
)

# ----------------------------------
# FILE UPLOAD
# ----------------------------------
if source == "Upload File":

    uploaded = st.file_uploader(
        "Upload FMCG Dataset (CSV / Excel)",
        type=["csv", "xlsx"]
    )

    if uploaded:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)

        st.session_state["df"] = df
        st.session_state["data_source"] = "upload"
        st.success(f"✅ Dataset loaded ({df.shape[0]} rows)")

# ----------------------------------
# SNOWFLAKE INGESTION
# ----------------------------------
else:
    st.subheader("❄️ Snowflake Connection")

    with st.form("snowflake_form"):
        account = st.text_input("Account")
        user = st.text_input("User")
        password = st.text_input("Password", type="password")
        warehouse = st.text_input("Warehouse")
        database = st.text_input("Database")
        schema = st.text_input("Schema")
        role = st.text_input("Role")
        table = st.text_input("Table Name")

        login = st.form_submit_button("Login & Load Data")

    if login:
        creds = {
            "account": account,
            "user": user,
            "password": password,
            "warehouse": warehouse,
            "database": database,
            "schema": schema,
            "role": role,
        }

        try:
            conn = get_snowflake_connection(creds)
            df = fetch_table_df(conn, database, schema, table)

            st.session_state["df"] = df
            st.session_state["data_source"] = "snowflake"

            st.success(f"✅ Snowflake data loaded ({df.shape[0]} rows)")
            st.info("📊 All dashboards are now active")

        except Exception as e:
            st.error(f"❌ Snowflake connection failed: {e}")
