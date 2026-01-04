import pandas as pd
from config import HIGH_CHURN_DAYS, MEDIUM_CHURN_DAYS


def churn_risk(df, outlet_col, date_col):
    if df is None or df.empty:
        return pd.DataFrame()

    temp = df[[outlet_col, date_col]].copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")

    last_order = temp.groupby(outlet_col)[date_col].max().reset_index()

    last_order["Days_Since_Last_Order"] = (
        pd.Timestamp.today() - last_order[date_col]
    ).dt.days

    def risk(days):
        if days > HIGH_CHURN_DAYS:
            return "High"
        elif days > MEDIUM_CHURN_DAYS:
            return "Medium"
        return "Low"

    last_order["Churn_Risk"] = last_order["Days_Since_Last_Order"].apply(risk)

    return last_order
