import pandas as pd


def prepare_sankey_data(
    df: pd.DataFrame,
    flow_columns: list,
    value_column: str,
    top_n: int | None = None
) -> pd.DataFrame:
    """
    Prepare Sankey source-target-value data with Top-N filtering
    """

    data = df[flow_columns + [value_column]].copy()

    data[value_column] = pd.to_numeric(
        data[value_column], errors="coerce"
    )
    data = data.dropna()

    sankey_rows = []

    for i in range(len(flow_columns) - 1):
        grouped = (
            data
            .groupby([flow_columns[i], flow_columns[i + 1]])[value_column]
            .sum()
            .reset_index()
        )

        grouped.columns = ["source", "target", "value"]
        sankey_rows.append(grouped)

    sankey_df = pd.concat(sankey_rows, ignore_index=True)

    if top_n:
        sankey_df = (
            sankey_df
            .sort_values("value", ascending=False)
            .head(top_n)
        )

    return sankey_df


def generate_ai_insight(sankey_df: pd.DataFrame) -> str:
    """
    Rule-based AI-style business explanation
    (Safe for production & interviews)
    """

    if sankey_df.empty:
        return "No significant flow patterns detected."

    top_flow = sankey_df.sort_values("value", ascending=False).iloc[0]
    total_value = sankey_df["value"].sum()

    contribution = (top_flow["value"] / total_value) * 100

    return f"""
    The strongest business flow is from **{top_flow['source']}**
    to **{top_flow['target']}**, contributing approximately
    **{contribution:.1f}%** of the total observed value.

    This indicates a **high dependency path**, which should be
    prioritized for operational stability, demand forecasting,
    and performance optimization.
    """
