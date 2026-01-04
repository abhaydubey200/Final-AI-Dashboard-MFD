import pandas as pd


def warehouse_kpis(df, warehouse_col, sales_col, qty_col):
    if df is None or df.empty:
        return pd.DataFrame()

    return (
        df.groupby(warehouse_col, as_index=False)
        .agg(
            Total_Sales=(sales_col, "sum"),
            Total_Quantity=(qty_col, "sum"),
            Orders=(sales_col, "count")
        )
        .fillna(0)
    )
