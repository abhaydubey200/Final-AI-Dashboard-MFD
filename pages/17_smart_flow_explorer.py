import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.smart_flow_utils import (
    prepare_sankey_data,
    generate_ai_insight
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Smart Flow Explorer",
    layout="wide"
)

st.title("🔗 Smart Flow Explorer")
st.caption("Actual vs Forecast enabled enterprise flow intelligence")

st.divider()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
if "dataframe" not in st.session_state:
    st.warning("Please upload data first.")
    st.stop()

df = st.session_state["dataframe"]

# --------------------------------------------------
# SIDEBAR CONTROLS
# --------------------------------------------------
with st.sidebar:
    st.header("Controls")

    metric_type = st.radio(
        "Metric Type",
        ["Actual Sales", "Forecast Sales"]
    )

    value_column = (
        "FORECAST_SALES"
        if metric_type == "Forecast Sales"
        and "FORECAST_SALES" in df.columns
        else "SALES_AMOUNT"
    )

    top_n = st.slider(
        "Top-N Flows",
        min_value=10,
        max_value=200,
        value=50,
        step=10
    )

    flow_type = st.selectbox(
        "Flow Structure",
        [
            "Sales Flow",
            "Warehouse Flow",
            "Customer Flow",
            "Order Status Flow"
        ]
    )

# --------------------------------------------------
# FLOW DEFINITIONS
# --------------------------------------------------
FLOW_MAP = {
    "Sales Flow": [
        "ZONE", "CITY", "OUTLET_CATEGORY",
        "SKU_PLACED", "ORDERSTATE"
    ],
    "Warehouse Flow": [
        "ZONE", "WAREHOUSE",
        "SKU_PLACED", "ORDERSTATE", "OUTLET_CATEGORY"
    ],
    "Customer Flow": [
        "CITY", "OUTLET_CATEGORY",
        "OUTLET_NAME", "SKU_PLACED", "ORDERSTATE"
    ],
    "Order Status Flow": [
        "WAREHOUSE", "ORDERSTATE",
        "REJECTED_ORDER_COMMENT",
        "SKU_PLACED", "OUTLET_NAME"
    ]
}

flow_columns = [
    c for c in FLOW_MAP[flow_type] if c in df.columns
]

if len(flow_columns) < 3:
    st.error("Insufficient columns for Sankey flow.")
    st.stop()

# --------------------------------------------------
# BUILD SANKEY DATA
# --------------------------------------------------
sankey_df = prepare_sankey_data(
    df=df,
    flow_columns=flow_columns,
    value_column=value_column,
    top_n=top_n
)

labels = pd.unique(
    sankey_df[["source", "target"]].values.ravel()
).tolist()

label_index = {v: i for i, v in enumerate(labels)}

# --------------------------------------------------
# SANKEY CHART
# --------------------------------------------------
fig = go.Figure(
    go.Sankey(
        node=dict(
            label=labels,
            pad=15,
            thickness=18
        ),
        link=dict(
            source=sankey_df["source"].map(label_index),
            target=sankey_df["target"].map(label_index),
            value=sankey_df["value"]
        )
    )
)

fig.update_layout(
    title=f"{flow_type} | {metric_type}",
    height=650
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# AI EXPLANATION LAYER
# --------------------------------------------------
st.divider()
st.subheader("🤖 AI Business Explanation")

insight = generate_ai_insight(sankey_df)
st.markdown(insight)

# --------------------------------------------------
# SUMMARY METRICS
# --------------------------------------------------
st.divider()
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Flow Value",
    f"{sankey_df['value'].sum():,.0f}"
)

col2.metric(
    "Unique Paths",
    sankey_df.shape[0]
)

col3.metric(
    "Flow Depth",
    len(flow_columns)
)

st.caption(
    "This page is designed for flow intelligence, dependency analysis, and executive decision support."
)
