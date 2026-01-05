import streamlit as st

st.set_page_config(page_title="Snowflake Data Explorer", layout="wide")
st.header("❄️ Snowflake Data Explorer")

df = st.session_state.get("df")
source = st.session_state.get("data_source")

if df is None or source != "snowflake":
    st.warning("Please load data from Snowflake first")
    st.stop()

st.write("### Dataset Preview")
st.dataframe(df, use_container_width=True)

st.write("### Column Summary")
st.write(df.describe(include="all"))
