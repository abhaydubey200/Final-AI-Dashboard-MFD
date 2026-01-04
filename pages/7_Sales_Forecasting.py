# pages/7_Warehouse_Logistics.py
# -------------------------------------------------
# Warehouse & Logistics Performance
# -------------------------------------------------

import streamlit as st

from utils.column_detector import auto_detect_columns
from utils.metrics import kpi_total_sales
from utils.visualizations import bar_top

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Warehouse & Logistics | DS Group",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Warehouse & Logistics Performance")
st.caption("Distribution efficiency, warehouse contribution & outlet flow")

st.divider()

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("📤 Please upload dataset or connect Snowflake.")
    st.stop()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

sales_col = cols.get("sales")
warehouse_col = cols.get("warehouse")
outlet_col = cols.get("outlet") or cols.get("store")

if not sales_col:
    st.error("❌ Sales column not detected.")
    st.stop()

# -------------------------------------------------
# KPIs
# -------------------------------------------------
k1, k2, k3 = st.columns(3)

k1.metric(
    "💰 Total Sales",
    f"{kpi_total_sales(df, sales_col):,.0f}"
)

k2.metric(
    "🏭 Warehouses",
    df[warehouse_col].nunique() if warehouse_col else "N/A"
)

k3.metric(
    "🏬 Outlets Served",
    df[outlet_col].nunique() if outlet_col else "N/A"
)

st.divider()

# -------------------------------------------------
# Warehouse Performance
# -------------------------------------------------
if warehouse_col:
    st.subheader("📊 Warehouse Contribution to Sales")

    st.plotly_chart(
        bar_top(
            df,
            warehouse_col,
            sales_col,
            title="Top Warehouses by Sales",
            top_n=15
        ),
        use_container_width=True
    )

else:
    st.warning("⚠ Warehouse column not found.")

# -------------------------------------------------
# Outlet Distribution
# -------------------------------------------------
if outlet_col:
    st.subheader("🏬 Top Outlets by Sales Volume")

    st.plotly_chart(
        bar_top(
            df,
            outlet_col,
            sales_col,
            title="Top Outlets by Sales",
            top_n=15
        ),
        use_container_width=True
    )
else:
    st.warning("⚠ Outlet / Store column not found.")

# -------------------------------------------------
# Operational Insight
# -------------------------------------------------
st.info(
    "📌 **Operational Insight:**\n\n"
    "- Identify warehouses driving maximum revenue\n"
    "- Detect outlet dependency on single warehouses\n"
    "- Optimize inventory placement for faster fulfillment"
)
