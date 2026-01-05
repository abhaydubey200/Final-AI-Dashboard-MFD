import streamlit as st
import pandas as pd

st.set_page_config(page_title="Snowflake SQL Studio", layout="wide")

st.title("🧪 Snowflake SQL Studio")
st.caption("Run secure read-only SQL queries and load results into the application")

# -------------------------------------------------
# AUTH CHECK
# -------------------------------------------------
if not st.session_state.get("snowflake_logged"):
    st.warning("🔐 Login via Snowflake Data Ingestion first")
    st.stop()

conn = st.session_state["snowflake_conn"]

# -------------------------------------------------
# SQL INPUT
# -------------------------------------------------
query = st.text_area(
    "Write SELECT query only",
    value="SELECT * FROM INFORMATION_SCHEMA.TABLES LIMIT 50",
    height=180
)

# -------------------------------------------------
# BUTTONS
# -------------------------------------------------
col1, col2 = st.columns(2)

run_preview = col1.button("▶ Run Query (Preview)")
load_data = col2.button("📥 Load Data into Application")

# -------------------------------------------------
# VALIDATION FUNCTION
# -------------------------------------------------
def validate_select_query(q: str):
    return q.strip().lower().startswith("select")

# -------------------------------------------------
# PREVIEW MODE
# -------------------------------------------------
if run_preview:
    if not validate_select_query(query):
        st.error("❌ Only SELECT queries are allowed")
        st.stop()

    try:
        df_preview = pd.read_sql(query, conn)
        df_preview = df_preview.astype(str)  # Arrow-safe

        st.success("✅ Query executed successfully (Preview)")
        st.dataframe(df_preview, width="stretch")

    except Exception as e:
        st.error(f"❌ Query execution failed: {e}")

# -------------------------------------------------
# LOAD INTO APPLICATION
# -------------------------------------------------
if load_data:
    if not validate_select_query(query):
        st.error("❌ Only SELECT queries are allowed")
        st.stop()

    try:
        df_final = pd.read_sql(query, conn)

        # Store into app session (GLOBAL)
        st.session_state["df"] = df_final
        st.session_state["data_source"] = "snowflake"
        st.session_state["active_table"] = "SQL Studio Result"

        st.success("🎉 Data successfully loaded into application!")
        st.info("You can now navigate to other dashboards")

        # Show sample
        st.dataframe(df_final.head(100).astype(str), width="stretch")

    except Exception as e:
        st.error(f"❌ Failed to load data into app: {e}")
