import streamlit as st
import pandas as pd

from config import SESSION_DF_KEY
from utils.column_detector import auto_detect_columns
from utils.business_signal_engine import detect_business_signals
from utils.priority_badges import priority_badge
from utils.ai_reasoning_engine import build_reasoned_response

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Executive Copilot",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Upload dataset first to activate AI Executive Copilot.")
    st.stop()

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("🤖 AI Executive Copilot")
st.caption("DS Group • CEO & Board-Level Intelligence Assistant")

st.divider()

# -------------------------------------------------
# AUTO PROFILE DATA
# -------------------------------------------------
cols = auto_detect_columns(df)
numeric_cols = [v for v in cols.values() if v and df[v].dtype != "object"]

profile = {
    "rows": len(df),
    "columns": df.shape[1],
    "numeric_cols": numeric_cols
}

# -------------------------------------------------
# SESSION CHAT MEMORY
# -------------------------------------------------
if "ai_chat" not in st.session_state:
    st.session_state.ai_chat = []

# -------------------------------------------------
# INPUT
# -------------------------------------------------
user_question = st.chat_input(
    "Ask anything about your business performance..."
)

# -------------------------------------------------
# AI RESPONSE ENGINE
# -------------------------------------------------
def ai_answer(question: str) -> str:
    q = question.lower()

    signals = detect_business_signals(df, numeric_cols)

    # ---------- CEO SUMMARY ----------
    if "summary" in q or "overview" in q:
        response = f"""
## 🧾 CEO EXECUTIVE SUMMARY

This dataset represents **{profile['rows']:,} business records** across key FMCG dimensions.

### Key Business Signals
"""

        for s in signals[:3]:
            response += f"""
{priority_badge(s['priority'])}  
**{s['metric']}**
• {s['signal']}
"""

        response += """
### Leadership Guidance
Focus attention on **high-volatility drivers**, execution consistency, and risk containment.

*Prepared for board-level discussion.*
"""
        return response

    # ---------- RISK ----------
    if "risk" in q:
        high_risk = [s for s in signals if s["priority"] == "High"]

        if not high_risk:
            return "🟢 No critical risks detected. Business performance is currently stable."

        response = "## 🚨 BUSINESS RISK ASSESSMENT\n"
        for s in high_risk:
            response += build_reasoned_response(s)

        return response

    # ---------- GENERAL ANALYSIS ----------
    response = "## 📊 BUSINESS ANALYSIS\n"
    for s in signals[:2]:
        response += build_reasoned_response(s)

    response += """
### Suggested Next Questions
• "Give CEO summary"
• "What are my biggest risks?"
• "Which metric needs attention?"
"""
    return response

# -------------------------------------------------
# CHAT LOOP
# -------------------------------------------------
if user_question:
    st.session_state.ai_chat.append(("user", user_question))
    answer = ai_answer(user_question)
    st.session_state.ai_chat.append(("ai", answer))

# -------------------------------------------------
# DISPLAY CHAT
# -------------------------------------------------
for role, msg in st.session_state.ai_chat:
    if role == "user":
        st.chat_message("user").markdown(msg)
    else:
        st.chat_message("assistant").markdown(msg)
