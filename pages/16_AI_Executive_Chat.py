import streamlit as st
from core.intent_engine import detect_intent
from core.metric_engine import compute_metrics
from core.response_formatter import format_response

st.title("🤖 AI Executive Assistant")
st.caption("Enterprise decision intelligence • Boardroom-ready • DS Group AI")

if "mfd_df" not in st.session_state:
    st.warning("Please upload dataset first.")
    st.stop()

df = st.session_state["mfd_df"]

query = st.text_input(
    "Ask anything about your MFD data",
    placeholder="e.g. total sales, outlet risk, sku performance"
)

if query:
    intent = detect_intent(query)
    metrics = compute_metrics(df, intent)
    response = format_response(metrics)

    st.subheader(response["header"])
    st.markdown(response["main"])

    with st.expander("Explain why"):
        st.markdown(response["explain"])

    st.caption(response["note"])

    st.markdown("### 🔍 Suggested follow-ups")
    st.markdown("""
    - Drill down by zone  
    - Compare brand performance  
    - Identify inactive outlets  
    - Analyze discount leakage  
    """)
