# utils/visualizations.py
# -------------------------------------------------
# Centralized Plotly Visual Components
# -------------------------------------------------

import plotly.express as px
import pandas as pd


# -------------------------------------------------
# Line Chart
# -------------------------------------------------
def line_sales_trend(df, date_col, sales_col, title="Sales Trend"):
    trend = (
        df
        .groupby(date_col)[sales_col]
        .sum()
        .reset_index()
        .sort_values(date_col)
    )

    fig = px.line(
        trend,
        x=date_col,
        y=sales_col,
        markers=True,
        title=title
    )

    fig.update_layout(
        xaxis_title=date_col,
        yaxis_title=sales_col
    )
    return fig


# -------------------------------------------------
# Bar Chart (TOP-N SAFE)
# -------------------------------------------------
def bar_top(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    title: str = "Top Categories",
    top_n: int = 10
):
    """
    SAFE top-N bar chart
    - top_n is always validated
    - never crashes Streamlit
    """

    # ---------- VALIDATION ----------
    if df.empty:
        return px.bar(title="No data available")

    if group_col not in df.columns or value_col not in df.columns:
        return px.bar(title="Required columns missing")

    try:
        top_n = int(top_n)
    except Exception:
        top_n = 10

    if top_n <= 0:
        top_n = 10

    # ---------- AGGREGATION ----------
    agg = (
        df
        .groupby(group_col, dropna=True)[value_col]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    if agg.empty:
        return px.bar(title="No aggregated data")

    # ---------- PLOT ----------
    fig = px.bar(
        agg,
        x=group_col,
        y=value_col,
        title=title,
        text=value_col
    )

    fig.update_layout(
        xaxis_title=group_col,
        yaxis_title=value_col
    )

    return fig


# -------------------------------------------------
# Heatmap
# -------------------------------------------------
def heatmap(df, x_col, y_col, value_col, title="Heatmap"):
    pivot_df = pd.pivot_table(
        df,
        index=y_col,
        columns=x_col,
        values=value_col,
        aggfunc="sum",
        fill_value=0
    )

    fig = px.imshow(
        pivot_df,
        labels=dict(x=x_col, y=y_col, color=value_col),
        text_auto=True,
        aspect="auto",
        title=title
    )
    return fig


# -------------------------------------------------
# Scatter
# -------------------------------------------------
def scatter_price_qty(df, price_col, qty_col, title="Price vs Quantity"):
    fig = px.scatter(
        df,
        x=price_col,
        y=qty_col,
        title=title,
        hover_data=df.columns
    )
    return fig


# -------------------------------------------------
# Pie
# -------------------------------------------------
def pie_chart(df, names_col, values_col, title="Share Distribution"):
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title
    )
    return fig
