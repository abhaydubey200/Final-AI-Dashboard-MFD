import streamlit as st
from config import SESSION_DF_KEY
from utils.column_detector import auto_detect_columns
from utils.ai_exec_engine import ExecutiveAIEngine

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="AI Executive Copilot",
    layout="wide"
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Upload data to activate AI Executive Copilot.")
    st.stop()

cols = auto_detect_columns(df)
ai_engine = ExecutiveAIEngine(df, cols)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("🧠 AI Executive Copilot")
st.markdown(
    "Enterprise-grade AI for **decision-ready answers** based on uploaded business data."
)

st.divider()

# -------------------------------------------------
# Chat Interface
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("Ask a business question (e.g. Total sales, Top SKUs)")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        response = ai_engine.execute(user_query)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
