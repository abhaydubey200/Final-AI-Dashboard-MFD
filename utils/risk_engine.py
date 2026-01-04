import pandas as pd

def outlet_risk_score(df, outlet_col, date_col, sales_col):
    df[date_col] = pd.to_datetime(df[date_col])

    latest_date = df[date_col].max()

    outlet_summary = (
        df.groupby(outlet_col)
        .agg(
            Total_Sales=(sales_col, "sum"),
            Last_Order=(date_col, "max"),
            Order_Count=(sales_col, "count")
        )
        .reset_index()
    )

    outlet_summary["Days_Inactive"] = (
        latest_date - outlet_summary["Last_Order"]
    ).dt.days

    def risk_label(row):
        if row["Days_Inactive"] > 60 or row["Total_Sales"] < outlet_summary["Total_Sales"].quantile(0.2):
            return "High"
        elif row["Days_Inactive"] > 30:
            return "Medium"
        else:
            return "Low"

    outlet_summary["Risk_Level"] = outlet_summary.apply(risk_label, axis=1)

    return outlet_summary


def warehouse_risk_score(df, warehouse_col, sales_col, qty_col):
    warehouse_summary = (
        df.groupby(warehouse_col)
        .agg(
            Total_Sales=(sales_col, "sum"),
            Total_Qty=(qty_col, "sum"),
            Orders=(sales_col, "count")
        )
        .reset_index()
    )

    sales_threshold = warehouse_summary["Total_Sales"].quantile(0.25)

    warehouse_summary["Risk_Level"] = warehouse_summary["Total_Sales"].apply(
        lambda x: "High" if x < sales_threshold else "Low"
    )

    return warehouse_summary
