import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta

from config import SESSION_DF_KEY, CURRENCY_SYMBOL

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Executive Assistant",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Upload dataset to activate AI Executive Assistant.")
    st.stop()

df.columns = [c.upper() for c in df.columns]
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"], errors="coerce")

# =========================================================
# SESSION CHAT MEMORY
# =========================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "suggested_followups" not in st.session_state:
    st.session_state.suggested_followups = []

# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <div style="padding:20px;border-radius:14px;background:#F5F7FA">
        <h2>🧠 AI Executive Assistant</h2>
        <p style="color:#333">
            Enterprise decision intelligence • Boardroom-ready • DS Group AI
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# INITIAL AUTO-SUGGEST (ONLY WHEN CHAT EMPTY)
# =========================================================
if not st.session_state.chat_history:
    st.markdown("### 💡 Suggested Questions")

    starters = [
        "Total sales",
        "Overall business performance",
        "Sales by month",
        "Top SKUs by revenue",
        "Outlet inactivity risk",
        "Revenue concentration risk",
        "Rejected orders summary",
    ]

    cols = st.columns(len(starters))
    for i, q in enumerate(starters):
        if cols[i].button(q):
            st.session_state.chat_history.append(("user", q))

# =========================================================
# CHAT INPUT
# =========================================================
user_input = st.chat_input("Ask anything about sales, outlets, SKUs, risks, performance...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

# =========================================================
# CORE ANALYTICS ENGINE
# =========================================================
def generate_response(question: str):
    q = question.lower()
    followups = []

    # ---------------- TOTAL SALES ----------------
    if "total sales" in q or "revenue" in q:
        total_sales = df["AMOUNT"].sum()

        response = f"""
📊 **Total Sales Overview**

Total recorded sales: **{CURRENCY_SYMBOL}{total_sales:,.0f}**

**Executive Note:**  
This represents the gross realized revenue across all orders in the dataset.
"""

        followups = [
            "Sales by month",
            "Top SKUs by revenue",
            "Discount impact on revenue",
        ]

    # ---------------- PERFORMANCE ----------------
    elif "performance" in q:
        response = f"""
📊 **Overall Business Performance**

• Total Sales: **{CURRENCY_SYMBOL}{df['AMOUNT'].sum():,.0f}**  
• Total Orders: **{df['ORDER_ID'].nunique():,}**  
• Active Outlets: **{df['OUTLET_ID'].nunique():,}**

**Executive Note:**  
Performance is evaluated using sales volume, order throughput, and outlet coverage.
"""

        followups = [
            "Best performing zone",
            "Worst performing outlet",
            "Outlet inactivity risk",
        ]

    # ---------------- MONTHLY SALES ----------------
    elif "month" in q:
        monthly = (
            df.groupby(df["ORDER_DATE"].dt.to_period("M"))["AMOUNT"]
            .sum()
            .reset_index()
        )

        last_growth = monthly["AMOUNT"].pct_change().iloc[-1] * 100 if len(monthly) > 1 else 0

        response = f"""
📈 **Monthly Sales Trend**

Latest month growth: **{last_growth:.2f}%**

**Executive Note:**  
Month-over-month trends highlight demand momentum and early risk signals.
"""

        followups = [
            "Sales drop analysis",
            "Seasonality impact",
            "Compare last two months",
        ]

    # ---------------- SKU PERFORMANCE ----------------
    elif "sku" in q:
        top_sku = (
            df.groupby("SKU_PLACED")["AMOUNT"]
            .sum()
            .sort_values(ascending=False)
            .head(1)
        )

        response = f"""
🏷 **SKU Performance Insight**

Top SKU by revenue: **{top_sku.index[0]}**  
Revenue: **{CURRENCY_SYMBOL}{top_sku.iloc[0]:,.0f}**

**Executive Note:**  
Revenue concentration at SKU level may indicate dependency risk.
"""

        followups = [
            "Revenue concentration risk",
            "Bottom performing SKUs",
            "SKU discount analysis",
        ]

    # ---------------- OUTLET RISK ----------------
    elif "outlet" in q and "risk" in q:
        last_date = df["ORDER_DATE"].max()
        inactive = df.groupby("OUTLET_ID")["ORDER_DATE"].max()
        inactive = inactive[inactive < last_date - timedelta(days=30)]

        response = f"""
⚠️ **Outlet Inactivity Risk**

Inactive outlets (>30 days): **{len(inactive)}**

**Executive Note:**  
Inactive outlets pose churn and revenue leakage risks.
"""

        followups = [
            "High potential outlet performance",
            "City-wise outlet contribution",
            "Outlet reactivation strategy",
        ]

    # ---------------- REJECTION ----------------
    elif "reject" in q:
        rejected = df[df["ORDERSTATE"].str.contains("reject", case=False, na=False)]
        rate = len(rejected) / len(df) * 100

        response = f"""
🚫 **Order Rejection Analysis**

Rejection rate: **{rate:.2f}%**

**Executive Note:**  
Rejections impact fulfillment efficiency and customer trust.
"""

        followups = [
            "Rejection reasons",
            "Warehouse rejection comparison",
            "Revenue impact of rejections",
        ]

    # ---------------- FALLBACK ----------------
    else:
        response = """
📊 **Executive Intelligence Ready**

Ask about:
• Sales & revenue  
• Orders & rejections  
• SKUs & brands  
• Outlets & geography  
• Risks & performance
"""

        followups = [
            "Total sales",
            "Overall performance",
            "Top SKUs by revenue",
        ]

    return response, followups

# =========================================================
# CHAT RENDERING
# =========================================================
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

# =========================================================
# PROCESS LAST USER MESSAGE
# =========================================================
if st.session_state.chat_history and st.session_state.chat_history[-1][0] == "user":
    question = st.session_state.chat_history[-1][1]
    answer, followups = generate_response(question)

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.chat_history.append(("assistant", answer))
    st.session_state.suggested_followups = followups

# =========================================================
# FOLLOW-UP SUGGESTIONS (COPILOT STYLE)
# =========================================================
if st.session_state.suggested_followups:
    st.markdown("### 🔍 Suggested follow-ups")
    cols = st.columns(len(st.session_state.suggested_followups))

    for i, q in enumerate(st.session_state.suggested_followups):
        if cols[i].button(q, key=f"follow_{i}"):
            st.session_state.chat_history.append(("user", q))
            st.rerun()
