# utils/forecasting.py
# -------------------------------------------------
# Robust Forecasting Utilities (Prophet + Fallback)
# -------------------------------------------------

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except Exception:
    PROPHET_AVAILABLE = False


def prepare_time_series(df, date_col, sales_col, freq="M"):
    """
    Prepare aggregated time series data with STANDARDIZED output.
    Returns columns: Date, Sales
    """

    temp = df[[date_col, sales_col]].copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")

    temp = (
        temp
        .groupby(pd.Grouper(key=date_col, freq=freq))[sales_col]
        .sum()
        .reset_index()
        .dropna()
    )

    temp = temp.rename(
        columns={
            date_col: "Date",
            sales_col: "Sales"
        }
    )

    temp = temp.sort_values("Date").reset_index(drop=True)

    return temp


def forecast_sales(ts_df: pd.DataFrame, periods: int = 6) -> pd.DataFrame:
    """
    Forecast future sales.
    Uses Prophet if available, otherwise falls back to Linear Regression.
    """

    # ----------------------------
    # Validate input
    # ----------------------------
    if "Date" not in ts_df.columns or "Sales" not in ts_df.columns:
        raise ValueError("Time series must contain 'Date' and 'Sales' columns")

    ts_df = ts_df.copy()

    # ----------------------------
    # TRY PROPHET (PRIMARY)
    # ----------------------------
    if PROPHET_AVAILABLE:
        try:
            prophet_df = ts_df.rename(
                columns={
                    "Date": "ds",
                    "Sales": "y"
                }
            )

            model = Prophet()
            model.fit(prophet_df)

            future = model.make_future_dataframe(
                periods=periods,
                freq="M"
            )

            forecast = model.predict(future)

            result = forecast[["ds", "yhat"]].tail(periods)
            result = result.rename(
                columns={
                    "ds": "Date",
                    "yhat": "Sales"
                }
            )

            return result.reset_index(drop=True)

        except Exception:
            # Prophet failed → fallback
            pass

    # ----------------------------
    # FALLBACK: Linear Regression
    # ----------------------------
    ts_df["t"] = np.arange(len(ts_df))

    X = ts_df[["t"]]
    y = ts_df["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    future_t = np.arange(len(ts_df), len(ts_df) + periods)
    future_sales = model.predict(future_t.reshape(-1, 1))

    future_dates = pd.date_range(
        start=ts_df["Date"].iloc[-1],
        periods=periods + 1,
        freq="M"
    )[1:]

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Sales": future_sales
    })

    return forecast_df.reset_index(drop=True)
