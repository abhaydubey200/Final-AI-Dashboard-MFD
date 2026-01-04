def total_sales(df, sales_col):
    if df is None or df.empty or sales_col not in df.columns:
        return 0.0
    return float(df[sales_col].sum())


def average_order_value(df, sales_col):
    if df is None or df.empty or sales_col not in df.columns:
        return 0.0
    return float(df[sales_col].mean())


def order_count(df):
    if df is None:
        return 0
    return int(len(df))
