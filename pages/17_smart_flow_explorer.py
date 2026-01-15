import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from config import SESSION_DF_KEY

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Smart Flow Explorer",
    layout="wide"
)

# =====================================================
# HEADER
# =====================================================
st.markdown("## 🔗 Smart Flow Explorer")
st.caption(
    "Enterprise value-flow intelligence • Boardroom-ready • DS Group AI"
)

st.divider()

# =====================================================
# SAFE DATA ACCESS
# =====================================================
def get_loaded_df():
    if SESSION_DF_KEY not in st.session_state:
        st.warning("📤 Please upload data from **Upload Dataset** page.")
        st.stop()

    df = st.session_state[SESSION_DF_KEY]

    if df is None or df.empty:
        st.warning("⚠️ Uploaded dataset is empty.")
        st.stop()

    return df.copy()

df = get_loaded_df()

# =====================================================
# REQUIRED COLUMNS
# =====================================================
required_cols = ["ZONE", "CITY", "WAREHOUSE", "BRAND", "CATEGORY", "AMOUNT"]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"❌ Required columns missing: {missing}")
    st.stop()

# =====================================================
# SIDEBAR — EXECUTIVE CONTROLS
# =====================================================
with st.sidebar:
    st.header("⚙️ Flow Configuration")

    st.caption("Hierarchy Selection")
    flow_levels = st.multiselect(
        "Business Flow Path",
        ["ZONE", "CITY", "WAREHOUSE", "BRAND", "CATEGORY"],
        default=["ZONE", "CITY", "BRAND"]
    )

    st.caption("Focus Scope")
    top_n = st.slider(
        "Top Value Flows",
        5, 40, 15
    )

    st.divider()
    st.caption("Mode")
    st.radio(
        "Analysis Type",
        ["Actual Sales"],
        disabled=True
    )

    if len(flow_levels) < 2:
        st.warning("Select at least 2 levels")

# =====================================================
# DATA PREPARATION
# =====================================================
flow_df = (
    df[flow_levels + ["AMOUNT"]]
    .dropna()
    .groupby(flow_levels, as_index=False)
    .agg({"AMOUNT": "sum"})
    .sort_values("AMOUNT", ascending=False)
    .head(top_n)
)

total_flow_value = flow_df["AMOUNT"].sum()
top_flow_value = flow_df.iloc[0]["AMOUNT"]
concentration_pct = (top_flow_value / total_flow_value) * 100

# =====================================================
# KPI STRIP
# =====================================================
k1, k2, k3, k4 = st.columns(4)

k1.metric("💰 Total Flow Value", f"₹{total_flow_value:,.0f}")
k2.metric("🔥 Top Flow Value", f"₹{top_flow_value:,.0f}")
k3.metric("⚠️ Concentration", f"{concentration_pct:.1f}%")
k4.metric("🔗 Flow Nodes", len(flow_levels))

st.divider()

# =====================================================
# SANKEY BUILD
# =====================================================
labels, sources, targets, values = [], [], [], []
label_index = {}

def idx(label):
    if label not in label_index:
        label_index[label] = len(labels)
        labels.append(label)
    return label_index[label]

for _, row in flow_df.iterrows():
    for i in range(len(flow_levels) - 1):
        s = f"{flow_levels[i]}: {row[flow_levels[i]]}"
        t = f"{flow_levels[i+1]}: {row[flow_levels[i+1]]}"

        sources.append(idx(s))
        targets.append(idx(t))
        values.append(row["AMOUNT"])

fig = go.Figure(
    go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            label=labels
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    )
)

fig.update_layout(
    title="Value Movement Across Business Layers",
    height=650,
    font_size=12
)

# =====================================================
# MAIN VISUAL
# =====================================================
st.subheader("📊 Business Value Flow Map")
st.plotly_chart(fig, use_container_width=True)

# =====================================================
# EXECUTIVE INTERPRETATION
# =====================================================
st.subheader("🧠 Executive Interpretation")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 🔍 Observation")
    st.markdown(
        f"""
        • Strong value concentration detected  
        • Dominant path controls **{concentration_pct:.1f}%** of flow  
        • Limited diversification across paths
        """
    )

with c2:
    st.markdown("### ⚠️ Why It Matters")
    st.markdown(
        """
        • High dependency increases risk exposure  
        • Disruption in one node impacts revenue  
        • Growth ceiling due to narrow channels
        """
    )

with c3:
    st.markdown("### ✅ Recommended Actions")
    st.markdown(
        """
        • Replicate top flows in other regions  
        • Strengthen secondary brands / cities  
        • Reduce single-path dependency
        """
    )

st.divider()

# =====================================================
# FOOTER NOTE
# =====================================================
st.caption(
    "Executive Note: This analysis is rule-based, deterministic, and derived "
    "directly from uploaded data. No external AI or prediction models used."
)
