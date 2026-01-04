import streamlit as st
from utils.data_loader import load_uploaded_file

st.markdown("<div class='page-title'>📤 Upload FMCG Dataset</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>CSV or Excel up to 2GB</div>", unsafe_allow_html=True)

# --------------------------------------------------
# Snowflake Lock
# --------------------------------------------------
if st.session_state.get("data_source") == "snowflake":
    st.warning("❄ Snowflake is connected. File upload is disabled.")
    st.stop()

# --------------------------------------------------
# File Upload
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Sales Dataset",
    type=["csv", "xlsx"]
)

if uploaded_file:
    df = load_uploaded_file(uploaded_file)

    if df is not None:
        st.success("✅ Dataset uploaded successfully")
        st.info(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
        st.dataframe(df.head(), use_container_width=True)
