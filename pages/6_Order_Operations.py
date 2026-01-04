from utils.risk_engine import warehouse_risk_score

# After loading df & detecting columns
warehouse_col = cols.get("warehouse")
qty_col = cols.get("quantity")

if warehouse_col and qty_col:
    st.subheader("🏬 Warehouse Risk Snapshot")

    w_df = warehouse_risk_score(df, warehouse_col, sales_col, qty_col)
    st.dataframe(w_df, use_container_width=True)
