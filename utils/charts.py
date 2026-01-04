import pandas as pd
import plotly.express as px


def _empty_fig(title=""):
    return px.line(title=title, template="plotly_white")


def line_sales_trend(df, date_col, sales_col):
    if df is None or df.empty or date_col not in df or sales_col not in df:
        return _empty_fig("Sales Trend")

    temp = df.copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")

    trend = temp.groupby(date_col, as_index=False)[sales_col].sum()

    return px.line(
        trend,
        x=date_col,
        y=sales_col,
        title="Sales Trend",
        markers=True,
        template="plotly_white"
    )


def bar_top(df, group_col, value_col, top_n=10, title="Top Categories"):
    if df is None or df.empty:
        return _empty_fig(title)

    agg = (
        df.groupby(group_col)[value_col]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    return px.bar(
        agg,
        x=group_col,
        y=value_col,
        text=value_col,
        title=title,
        template="plotly_white"
    )


def heatmap(df, x_col, y_col, value_col, title="Heatmap"):
    if df is None or df.empty:
        return _empty_fig(title)

    pivot = pd.pivot_table(
        df,
        index=y_col,
        columns=x_col,
        values=value_col,
        aggfunc="sum",
        fill_value=0
    )

    return px.imshow(
        pivot,
        title=title,
        text_auto=True,
        aspect="auto",
        template="plotly_white"
    )


def scatter_price_qty(df, price_col, qty_col, title="Price vs Quantity"):
    if df is None or df.empty:
        return _empty_fig(title)

    return px.scatter(
        df,
        x=price_col,
        y=qty_col,
        title=title,
        opacity=0.7,
        template="plotly_white"
    )


def pie_chart(df, names_col, values_col, title="Category Share"):
    if df is None or df.empty:
        return _empty_fig(title)

    return px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
        template="plotly_white"
    )
