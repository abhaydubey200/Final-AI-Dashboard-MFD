import pandas as pd


def prepare_daily_sales_df(df, date_col, sales_col):
    """
    Enterprise-safe daily sales preparation utility.

    Guarantees:
    - Stable column names
    - Numeric-only Plotly inputs
    - No Pandas groupby column loss
    - No Streamlit Cloud crashes
    """

    if df is None or df.empty:
        raise ValueError("Dataset is empty")

    if date_col not in df.columns:
        raise ValueError(f"Missing date column: {date_col}")

    if sales_col not in df.columns:
        raise ValueError(f"Missing sales column: {sales_col}")

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
        .groupby(pd.Grouper(key=date_col, freq="D"))[sales_col]
        .sum()
        .reset_index()
    )

    # -----------------------------
    # CANONICAL COLUMN NAMES
    # -----------------------------
    daily_df.columns = ["Date", "Daily_Sales"]

    # -----------------------------
    # SORTING
    # -----------------------------
    daily_df = daily_df.sort_values("Date")

    # -----------------------------
    # ROLLING METRICS
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
