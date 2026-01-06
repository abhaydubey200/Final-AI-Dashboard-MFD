import pandas as pd
import numpy as np


def prepare_daily_sales_df(df, date_col, sales_col):
    """
    Enterprise-safe daily sales preparation
    - Cleans dates
    - Ensures numeric sales
    - Aggregates daily
    - Adds rolling averages
    - Prevents Plotly wide-form crashes
    """

    data = df.copy()

    # -----------------------------
    # DATE NORMALIZATION
    # -----------------------------
    data[date_col] = pd.to_datetime(
        data[date_col],
        errors="coerce"
    )

    data = data.dropna(subset=[date_col])

    # -----------------------------
    # SALES NORMALIZATION
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

    # -----------------------------
    # DAILY AGGREGATION
    # -----------------------------
    daily_df = (
        data
        .groupby(pd.Grouper(key=date_col, freq="D"), as_index=False)
        .agg({"{}".format(sales_col): "sum"})
    )

    daily_df.rename(
        columns={sales_col: "Daily_Sales"},
        inplace=True
    )

    # -----------------------------
    # SORTING
    # -----------------------------
    daily_df = daily_df.sort_values(date_col)

    # -----------------------------
    # ROLLING AVERAGES
    # -----------------------------
    daily_df["7D_Rolling_Avg"] = (
        daily_df["Daily_Sales"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    daily_df["14D_Rolling_Avg"] = (
        daily_df["Daily_Sales"]
        .rolling(window=14, min_periods=1)
        .mean()
    )

    return daily_df
