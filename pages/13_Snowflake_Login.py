import streamlit as st
from utils.snowflake_connector import fetch_snowflake_data
from utils.data_loader import load_from_snowflake

st.markdown("<div class='page-title'>❄ Snowflake Data Connector</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Secure enterprise data ingestion</div>", unsafe_allow_html=True)

# --------------------------------------------------
# Login Form
# --------------------------------------------------
with st.form("snowflake_form"):
    col1, col2 = st.columns(2)

    with col1:
        account = st.text_input("Account")
        user = st.text_input("User")
        password = st.text_input("Password", type="password")

    with col2:
        warehouse = st.text_input("Warehouse")
        database = st.text_input("Database")
        schema = st.text_input("Schema")
        table = st.text_input("Table")

    submitted = st.form_submit_button("🔐 Login & Load Data")

# --------------------------------------------------
# Login Action
# --------------------------------------------------
if submitted:
    try:
        df = fetch_snowflake_data(
            account, user, password,
            warehouse, database, schema, table
        )

        load_from_snowflake(df)

        st.success("✅ Snowflake data loaded successfully")

    except Exception as e:
        st.error(f"❌ Connection failed: {e}")

# --------------------------------------------------
# Controls
# --------------------------------------------------
if st.session_state.get("snowflake_connected"):
    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        if st.button("🔄 Refresh Data"):
            st.experimental_rerun()

    with c2:
        if st.button("🚪 Logout Snowflake"):
            st.session_state["df"] = None
            st.session_state["snowflake_connected"] = False
            st.session_state["data_source"] = "upload"
            st.success("Logged out successfully")
            st.experimental_rerun()
