import pandas as pd


def preprocess(df, date_col):
    if df is None or df.empty or date_col not in df:
        return df

    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])

    df["Year"] = df[date_col].dt.year
    df["Month"] = df[date_col].dt.month
    df["MonthName"] = df[date_col].dt.strftime("%b")

    return df
