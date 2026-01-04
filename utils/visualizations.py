import plotly.express as px
import pandas as pd


def line_sales_trend(df, date_col, sales_col, title="Sales Trend"):
    if df is None or df.empty:
        return px.line(title=title)

    temp = df.copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")

    agg = temp.groupby(date_col, as_index=False)[sales_col].sum()

    fig = px.line(
        agg,
        x=date_col,
        y=sales_col,
        title=title,
        markers=True,
        template="plotly_white"
    )
    return fig


def bar_top(df, group_col, value_col, top_n=10, title="Top Performance"):
    if df is None or df.empty:
        return px.bar(title=title)

    agg = (
        df.groupby(group_col)[value_col]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        agg,
        x=group_col,
        y=value_col,
        text=value_col,
        title=title,
        template="plotly_white"
    )
    return fig


def pie_chart(df, names_col, values_col, title="Share"):
    if df is None or df.empty:
        return px.pie(title=title)

    return px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
        template="plotly_white"
    )
