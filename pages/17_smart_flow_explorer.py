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
# DARK UI STYLING
# =====================================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# HEADER
# =====================================================
st.markdown("## 🔗 Smart Flow Explorer")
st.caption(
    "Enterprise flow intelligence • High-contrast analytical view"
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
# SIDEBAR — CONTROLS
# =====================================================
with st.sidebar:
    st.header("⚙️ Flow Controls")

    flow_levels = st.multiselect(
        "Flow Path (Left → Right)",
        ["ZONE", "CITY", "WAREHOUSE", "BRAND", "CATEGORY"],
        default=["ZONE", "CITY", "BRAND"]
    )

    top_n = st.slider(
        "Top Value Paths",
        5, 40, 20
    )

    if len(flow_levels) < 2:
        st.warning("Select at least 2 flow levels")

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

# =====================================================
# SANKEY CONSTRUCTION
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
        s = f"{row[flow_levels[i]]}"
        t = f"{row[flow_levels[i + 1]]}"

        sources.append(idx(s))
        targets.append(idx(t))
        values.append(row["AMOUNT"])

fig = go.Figure(
    go.Sankey(
        arrangement="snap",
        node=dict(
            pad=25,
            thickness=22,
            line=dict(color="#AAAAAA", width=0.5),
            label=labels,
            color="#1F7AE0"
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color="rgba(0, 200, 200, 0.6)"
        )
    )
)

fig.update_layout(
    title="Value Flow Across Business Dimensions",
    font=dict(size=13, color="white"),
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    height=700
)

# =====================================================
# DISPLAY
# =====================================================
st.plotly_chart(fig, use_container_width=True)

# =====================================================
# CHART EXPLANATION (ONLY)
# =====================================================
st.markdown("### 📌 How to Read This Chart")

st.markdown(
    """
- **Each block** represents a business entity (Zone, City, Brand, etc.)
- **Flow thickness** represents total sales value movement
- **Left → Right** shows how value travels across dimensions
- **Wider paths** indicate dominant business routes
- **Narrow paths** highlight underutilized or fragmented flows
"""
)

st.caption(
    "Note: This visualization is generated directly from uploaded transactional data. "
    "No forecasting or AI assumptions are applied."
)
