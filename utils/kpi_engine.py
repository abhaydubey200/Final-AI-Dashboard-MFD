import pandas as pd

def calculate_growth(current, previous):
    if previous == 0 or pd.isna(previous):
        return 0
    return round(((current - previous) / previous) * 100, 2)


def generate_kpis(df, date_col, sales_col):
    df[date_col] = pd.to_datetime(df[date_col])

    latest_month = df[date_col].max().to_period("M")
    prev_month = latest_month - 1

    current_df = df[df[date_col].dt.to_period("M") == latest_month]
    previous_df = df[df[date_col].dt.to_period("M") == prev_month]

    current_sales = current_df[sales_col].sum()
    previous_sales = previous_df[sales_col].sum()

    mom_growth = calculate_growth(current_sales, previous_sales)

    ytd_sales = df[df[date_col].dt.year == latest_month.year][sales_col].sum()

    return {
        "Current Month Sales": current_sales,
        "Previous Month Sales": previous_sales,
        "MoM Growth %": mom_growth,
        "YTD Sales": ytd_sales
    }
