import pandas as pd


def prepare_daily_sales_df(df: pd.DataFrame, date_col: str, sales_col: str):
    """
    Bulletproof daily sales preparation
    - Never returns empty silently
    - Guarantees Plotly-safe numeric columns
    """

    if df is None or df.empty:
        raise ValueError("Dataset is empty")

    if date_col not in df.columns or sales_col not in df.columns:
        raise KeyError("Required columns missing")

    data = df[[date_col, sales_col]].copy()

    # -----------------------------
    # DATE CLEANING
    # -----------------------------
    data[date_col] = pd.to_datetime(
        data[date_col],
        errors="coerce",
        utc=False
    )

    data = data.dropna(subset=[date_col])

    # -----------------------------
    # SALES CLEANING
    # -----------------------------
    data[sales_col] = (
        data[sales_col]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    data[sales_col] = pd.to_numeric(
        data[sales_col],
        errors="coerce"
    )

    data = data.dropna(subset=[sales_col])

    if data.empty:
        raise ValueError("No valid daily sales data after cleaning")

    # -----------------------------
    # DAILY AGGREGATION
    # -----------------------------
    daily_df = (
        data
        .groupby(pd.Grouper(key=date_col, freq="D"))
        .sum(numeric_only=True)
        .reset_index()
    )

    daily_df.rename(columns={sales_col: "Daily_Sales"}, inplace=True)

    # -----------------------------
    # SORT + ROLLING
    # -----------------------------
    daily_df = daily_df.sort_values(date_col)

    daily_df["7D_Rolling_Avg"] = (
        daily_df["Daily_Sales"]
        .rolling(7, min_periods=1)
        .mean()
    )

    daily_df["14D_Rolling_Avg"] = (
        daily_df["Daily_Sales"]
        .rolling(14, min_periods=1)
        .mean()
    )

    return daily_df
