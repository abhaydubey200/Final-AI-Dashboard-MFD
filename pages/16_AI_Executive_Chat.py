import streamlit as st
from config import SESSION_DF_KEY
from utils.column_detector import auto_detect_columns
from utils.ai_exec_intent import detect_intent
from utils.ai_exec_reasoner import ReasoningEngine
from utils.ai_exec_responder import ResponseComposer

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Executive Chat",
    layout="wide"
)

# --------------------------------------------------
# DATA GUARD
# --------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Upload dataset or connect Snowflake to activate Executive AI.")
    st.stop()

cols = auto_detect_columns(df)

# --------------------------------------------------
# INIT AI SYSTEM
# --------------------------------------------------
reasoner = ReasoningEngine(df, cols)
responder = ResponseComposer()

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🤖 AI Executive Assistant")
st.caption(
    "Enterprise decision intelligence • Boardroom-ready • DS Group AI"
)

st.divider()

# --------------------------------------------------
# CHAT MEMORY
# --------------------------------------------------
if "ai_chat" not in st.session_state:
    st.session_state.ai_chat = []

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------
user_input = st.chat_input(
    "Ask anything about sales, risk, performance, strategy, or scenarios..."
)

if user_input:
    st.session_state.ai_chat.append(("user", user_input))

    intent = detect_intent(user_input)
    reasoning = reasoner.run(intent, user_input)
    final_response = responder.compose(intent, reasoning)

    st.session_state.ai_chat.append(("assistant", final_response))

# --------------------------------------------------
# CHAT RENDER
# --------------------------------------------------
for role, message in st.session_state.ai_chat:
    with st.chat_message(role):
        st.markdown(message)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption("DS Group • AI Executive Intelligence Platform")
