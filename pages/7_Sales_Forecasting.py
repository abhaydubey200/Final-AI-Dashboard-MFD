# pages/5_Field_Force_Productivity.py
# -------------------------------------------------
# Field Force Productivity Dashboard
# -------------------------------------------------

import streamlit as st
from utils.column_detector import auto_detect_columns
from utils.visualizations import bar_top

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Field Force Productivity | DS Group",
    page_icon="🧑‍💼",
    layout="wide"
)

st.title("🧑‍💼 Field Force Productivity")
st.caption("Evaluate sales representative efficiency & contribution")

st.divider()

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
df = st.session_state.get("df")

if df is None or df.empty:
    st.warning("📤 Upload dataset or connect Snowflake first.")
    st.stop()

# -------------------------------------------------
# Auto Detect Columns
# -------------------------------------------------
cols = auto_detect_columns(df)

rep_col = cols.get("rep")
sales_col = cols.get("sales")
qty_col = cols.get("quantity")

# -------------------------------------------------
# Validation
# -------------------------------------------------
if not rep_col:
    st.warning("⚠ Sales representative column not detected.")
    st.stop()

if not sales_col:
    st.warning("⚠ Sales column not detected.")
    st.stop()

# -------------------------------------------------
# Charts
# -------------------------------------------------
st.subheader("📊 Sales Contribution by Sales Representative")

st.plotly_chart(
    bar_top(
        df,
        rep_col,
        sales_col,
        title="Sales per Sales Representative",
        top_n=15
    ),
    use_container_width=True
)

# -------------------------------------------------
# Quantity Productivity
# -------------------------------------------------
if qty_col:
    st.subheader("📦 Quantity Sold by Sales Representative")

    st.plotly_chart(
        bar_top(
            df,
            rep_col,
            qty_col,
            title="Quantity Sold per Sales Representative",
            top_n=15
        ),
        use_container_width=True
    )
else:
    st.info("ℹ Quantity column not available — showing sales-based productivity only.")

# -------------------------------------------------
# Business Insight
# -------------------------------------------------
st.info(
    "📌 **Insights:**\n\n"
    "- Identify top-performing sales representatives\n"
    "- Detect underperformers for coaching\n"
    "- Align incentives with actual field contribution"
)
