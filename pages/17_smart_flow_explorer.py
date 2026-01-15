import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from config import SESSION_DF_KEY

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Smart Flow Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔗 Smart Flow Explorer")
st.caption("Enterprise Flow Intelligence • Actual vs Forecast • DS Group")

# =====================================================
# SAFE DATA LOADER (SINGLE SOURCE OF TRUTH)
# =====================================================
def get_loaded_df() -> pd.DataFrame:
    if SESSION_DF_KEY not in st.session_state:
        st.warning("📤 Please upload data from **Upload Dataset** page first.")
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
REQUIRED_COLS = [
    "ZONE",
    "CITY",
    "WAREHOUSE",
    "BRAND",
    "CATEGORY",
    "AMOUNT"
]

missing_cols = [c for c in REQUIRED_COLS if c not in df.columns]

if missing_cols:
    st.error(f"❌ Missing required columns: {missing_cols}")
    st.stop()

# =====================================================
# SIDEBAR CONTROLS
# =====================================================
with st.sidebar:
    st.header("⚙️ Flow Controls")

    top_n = st.slider(
        "Top-N Flow Limit",
        min_value=5,
        max_value=50,
        value=15
    )

    analysis_mode = st.radio(
        "Analysis Mode",
        ["Actual Sales"],
        horizontal=True
    )

    st.divider()

    st.caption("Flow Path")
    flow_levels = st.multiselect(
        "Select flow hierarchy",
        ["ZONE", "CITY", "WAREHOUSE", "BRAND", "CATEGORY"],
        default=["ZONE", "CITY", "BRAND"]
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

# =====================================================
# SANKEY NODE & LINK BUILDER
# =====================================================
labels = []
label_index = {}
sources = []
targets = []
values = []

def get_label_index(label):
    if label not in label_index:
        label_index[label] = len(labels)
        labels.append(label)
    return label_index[label]

for _, row in flow_df.iterrows():
    for i in range(len(flow_levels) - 1):
        src = f"{flow_levels[i]}: {row[flow_levels[i]]}"
        tgt = f"{flow_levels[i+1]}: {row[flow_levels[i+1]]}"

        src_idx = get_label_index(src)
        tgt_idx = get_label_index(tgt)

        sources.append(src_idx)
        targets.append(tgt_idx)
        values.append(row["AMOUNT"])

# =====================================================
# SANKEY CHART
# =====================================================
fig = go.Figure(
    go.Sankey(
        node=dict(
            pad=15,
            thickness=18,
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
    title="🔁 Business Flow Mapping (Value Movement)",
    font_size=11,
    height=650
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# AI-STYLE EXPLANATION (RULE-BASED)
# =====================================================
st.subheader("🧠 Executive Interpretation")

top_flow = flow_df.iloc[0]

st.markdown(
    f"""
**Key Observation**
- Highest value flow detected through **{flow_levels[0]} → {flow_levels[-1]}**
- Top contributor: **{top_flow[flow_levels[-1]]}**
- Value impact: **₹{top_flow['AMOUNT']:,.0f}**

**Strategic Insight**
- Revenue concentration visible in limited paths
- Indicates dependency on specific regions / brands
- Opportunity to diversify flow channels

**Action Recommendation**
- Strengthen mid-tier flows
- Reduce over-reliance on dominant nodes
- Replicate high-performing paths across regions
"""
)

st.caption(
    "Executive Note: This insight is generated deterministically from uploaded data. "
    "No AI models or external APIs were used."
)
