import streamlit as st
import pandas as pd
import numpy as np

from config import SESSION_DF_KEY, HIGH_CHURN_DAYS, ENABLE_AI_SUMMARY
from utils.column_detector import auto_detect_columns
from utils.churn_analysis import churn_risk

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Actionable Business Insights",
    layout="wide",
)

# =================================================
# LOAD DATA
# =================================================
df = st.session_state.get(SESSION_DF_KEY)

if df is None or df.empty:
    st.warning("📥 Upload dataset or connect Snowflake to activate insights.")
    st.stop()

# =================================================
# HEADER
# =================================================
st.markdown("## 🧠 Actionable Business Insights")
st.caption(
    "Decision-ready insights highlighting **business risks, growth opportunities, and executive actions**."
)

st.divider()

# =================================================
# AUTO COLUMN DETECTION
# =================================================
cols = auto_detect_columns(df)

date_col = cols.get("date")
sales_col = cols.get("sales")
sku_col = cols.get("sku")
outlet_col = cols.get("outlet")

if not date_col or not sales_col:
    st.error("❌ Date & Sales columns are mandatory for insights.")
    st.stop()

df[date_col] = pd.to_datetime(df[date_col])

# =================================================
# EXECUTIVE KPI SNAPSHOT
# =================================================
monthly_sales_df = (
    df
    .groupby(pd.Grouper(key=date_col, freq="M"))[sales_col]
    .sum()
    .reset_index()
)

total_sales = df[sales_col].sum()
avg_monthly_sales = monthly_sales_df[sales_col].mean()
latest_month_sales = monthly_sales_df[sales_col].iloc[-1]

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Revenue", f"₹{total_sales:,.0f}")
k2.metric("Avg Monthly Revenue", f"₹{avg_monthly_sales:,.0f}")
k3.metric("Latest Month Revenue", f"₹{latest_month_sales:,.0f}")

if sku_col:
    sku_sales = df.groupby(sku_col)[sales_col].sum().sort_values(ascending=False)
    top_sku_share = sku_sales.iloc[0] / sku_sales.sum() * 100
    k4.metric("Top SKU Dependency", f"{top_sku_share:.1f}%")
else:
    top_sku_share = None
    k4.metric("Top SKU Dependency", "N/A")

st.divider()

# =================================================
# INSIGHT ENGINES WITH PRIORITY
# =================================================
risks = []
opportunities = []
actions = []

priority_score = 0  # used for CEO summary

# -------------------------------------------------
# SALES MOMENTUM RISK
# -------------------------------------------------
monthly_sales_df["Growth_%"] = monthly_sales_df[sales_col].pct_change() * 100
recent_growth = monthly_sales_df["Growth_%"].iloc[-1]

if recent_growth < -5:
    risks.append(("High", "📉 Sales momentum has declined sharply (>5%) in the most recent month."))
    actions.append("Conduct immediate review of pricing, stock availability, and distributor coverage.")
    priority_score += 3
elif recent_growth < 0:
    risks.append(("Medium", "⚠️ Sales growth has turned negative, indicating early demand softening."))
    actions.append("Monitor distributor orders and field execution closely.")
    priority_score += 2

# -------------------------------------------------
# SKU CONCENTRATION RISK
# -------------------------------------------------
if sku_col and top_sku_share and top_sku_share > 40:
    risks.append(("High", f"🧩 Revenue concentration risk detected — top SKU contributes {top_sku_share:.1f}% of sales."))
    actions.append("Reduce dependency by pushing secondary SKUs and bundle strategies.")
    priority_score += 3

# -------------------------------------------------
# OUTLET CHURN RISK
# -------------------------------------------------
if outlet_col:
    churn_df = churn_risk(df, outlet_col, date_col)
    high_risk_outlets = (churn_df["Churn_Risk"] == "High").sum()

    if high_risk_outlets > 0:
        risks.append(("High", f"🚨 {high_risk_outlets} outlets inactive for over {HIGH_CHURN_DAYS} days."))
        actions.append("Launch outlet reactivation schemes and optimize beat planning.")
        priority_score += 3

# -------------------------------------------------
# GROWTH OPPORTUNITY
# -------------------------------------------------
if monthly_sales_df["Growth_%"].mean() > 3:
    opportunities.append(("Medium", "🚀 Consistent average monthly growth above 3%."))
    actions.append("Scale production and distributor allocation to capture momentum.")
    priority_score += 1

# =================================================
# PRIORITY BADGE
# =================================================
if priority_score >= 7:
    priority_level = "🔴 HIGH PRIORITY"
elif priority_score >= 4:
    priority_level = "🟠 MEDIUM PRIORITY"
else:
    priority_level = "🟢 LOW PRIORITY"

st.markdown(f"### Executive Priority Level: **{priority_level}**")

st.divider()

# =================================================
# DISPLAY INSIGHTS
# =================================================
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("🚨 Key Risks")
    if risks:
        for p, r in risks:
            st.markdown(f"- **[{p}]** {r}")
    else:
        st.success("No material risks identified.")

with c2:
    st.subheader("🌱 Opportunities")
    if opportunities:
        for p, o in opportunities:
            st.markdown(f"- **[{p}]** {o}")
    else:
        st.info("No immediate growth opportunities identified.")

with c3:
    st.subheader("📌 Recommended Actions")
    if actions:
        for a in set(actions):
            st.markdown(f"- {a}")
    else:
        st.success("Current strategy appears optimal.")

# =================================================
# AI-GENERATED CEO SUMMARY (TEXT ONLY)
# =================================================
if ENABLE_AI_SUMMARY:
    st.divider()
    st.subheader("🤖 AI-Generated CEO Summary")

    summary_text = f"""
**Overall Business Health:** {priority_level.replace('🔴','').replace('🟠','').replace('🟢','')}

• Total revenue stands at ₹{total_sales:,.0f} with latest month contributing ₹{latest_month_sales:,.0f}.
• Sales momentum shows {'decline' if recent_growth < 0 else 'stability'} in the most recent period.
• Revenue concentration {'is high' if top_sku_share and top_sku_share > 40 else 'remains within acceptable limits'}.
• Outlet churn risk requires {'immediate attention' if priority_score >= 7 else 'continuous monitoring'}.

**CEO Recommendation:**  
Prioritize execution discipline in the short term while protecting growth levers. Immediate focus should be on demand recovery, outlet reactivation, and SKU portfolio balance.
"""
    st.success(summary_text)

# =================================================
# FOOTER
# =================================================
st.caption("Actionable Insights Engine • DS Group FMCG Executive Intelligence Platform")
