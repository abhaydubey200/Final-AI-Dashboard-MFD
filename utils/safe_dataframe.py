import pandas as pd


def prepare_daily_sales_df(df: pd.DataFrame, date_col: str, sales_col: str) -> pd.DataFrame:
    """
    Enterprise-safe daily aggregation
    - Date normalization
    - Numeric safety
    - Daily aggregation
    - Rolling averages
    """

    data = df.copy()

    # --------------------
    # DATE NORMALIZATION
    # --------------------
    data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
    data = data.dropna(subset=[date_col])

    # --------------------
    # SALES NORMALIZATION
    # --------------------
    data[sales_col] = (
        data[sales_col]
        .astype(str)
        .str.replace(",", "", regex=False)
    )
    data[sales_col] = pd.to_numeric(data[sales_col], errors="coerce")
    data = data.dropna(subset=[sales_col])

    # --------------------
    # DAILY AGGREGATION
    # --------------------
    daily_df = (
        data
        .groupby(pd.Grouper(key=date_col, freq="D"))[sales_col]
        .sum()
        .reset_index()
    )

    daily_df.columns = ["Date", "Daily_Sales"]
    daily_df = daily_df.sort_values("Date")

    # --------------------
    # ROLLING AVERAGES
    # --------------------
    daily_df["7D_Rolling_Avg"] = daily_df["Daily_Sales"].rolling(7, min_periods=1).mean()
    daily_df["14D_Rolling_Avg"] = daily_df["Daily_Sales"].rolling(14, min_periods=1).mean()

    return daily_df
