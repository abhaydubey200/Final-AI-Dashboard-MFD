import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def prepare_time_series(df, date_col, sales_col, freq="MS"):
    temp = df[[date_col, sales_col]].copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
    temp = temp.dropna()

    ts = (
        temp.groupby(pd.Grouper(key=date_col, freq=freq))[sales_col]
        .sum()
        .reset_index()
    )

    ts.columns = ["Date", "Sales"]
    ts["t"] = np.arange(len(ts))

    return ts


def forecast_sales(ts_df, periods=12):
    X = ts_df[["t"]]
    y = ts_df["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    future_t = np.arange(len(ts_df), len(ts_df) + periods)
    preds = model.predict(future_t.reshape(-1, 1))

    future_dates = pd.date_range(
        start=ts_df["Date"].max(),
        periods=periods + 1,
        freq="MS"
    )[1:]

    return pd.DataFrame({
        "Date": future_dates,
        "Sales": preds
    })
