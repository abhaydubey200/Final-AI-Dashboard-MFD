import streamlit as st

def kpi_card(title, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def ai_summary(text):
    st.markdown(
        f"""
        <div class="ai-box">
            <div class="ai-title">🧠 AI Executive Summary</div>
            <div>{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
