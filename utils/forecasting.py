import pandas as pd
import numpy as np

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except Exception:
    PROPHET_AVAILABLE = False

from sklearn.linear_model import LinearRegression


def prepare_time_series(df, date_col, sales_col, freq="M"):
    if df is None or df.empty:
        return pd.DataFrame()

    if date_col not in df.columns or sales_col not in df.columns:
        return pd.DataFrame()

    temp = df[[date_col, sales_col]].copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
    temp = temp.dropna()

    ts = (
        temp
        .groupby(pd.Grouper(key=date_col, freq=freq))[sales_col]
        .sum()
        .reset_index()
    )

    ts.rename(columns={date_col: "ds", sales_col: "y"}, inplace=True)
    return ts


def forecast_sales(ts_df, periods=12):
    if ts_df is None or ts_df.empty:
        return pd.DataFrame()

    # ---------------- Prophet (Primary) ----------------
    if PROPHET_AVAILABLE and len(ts_df) >= 6:
        model = Prophet()
        model.fit(ts_df)

        future = model.make_future_dataframe(periods=periods, freq="M")
        forecast = model.predict(future)

        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]

    # ---------------- Linear Regression (Fallback) ----------------
    ts_df = ts_df.copy()
    ts_df["t"] = np.arange(len(ts_df))

    X = ts_df[["t"]]
    y = ts_df["y"]

    model = LinearRegression()
    model.fit(X, y)

    future_t = np.arange(len(ts_df), len(ts_df) + periods)
    future_y = model.predict(future_t.reshape(-1, 1))

    future_dates = pd.date_range(
        start=ts_df["ds"].iloc[-1],
        periods=periods + 1,
        freq="M"
    )[1:]

    return pd.DataFrame({
        "ds": future_dates,
        "yhat": future_y
    })
