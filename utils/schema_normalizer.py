import pandas as pd
from utils.column_detector import auto_detect_columns


def normalize_dataframe_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize dataframe column names so ALL dashboards
    work consistently for Upload + Snowflake.
    """

    if df is None or df.empty:
        return df

    cols = auto_detect_columns(df)

    rename_map = {}

    if cols.get("date"):
        rename_map[cols["date"]] = "DATE"

    if cols.get("sales"):
        rename_map[cols["sales"]] = "SALES"

    if cols.get("quantity"):
        rename_map[cols["quantity"]] = "QUANTITY"

    if cols.get("brand"):
        rename_map[cols["brand"]] = "BRAND"

    if cols.get("sku"):
        rename_map[cols["sku"]] = "SKU"

    if cols.get("rep"):
        rename_map[cols["rep"]] = "SALES_REP"

    if cols.get("outlet"):
        rename_map[cols["outlet"]] = "OUTLET"

    df = df.rename(columns=rename_map)

    return df
