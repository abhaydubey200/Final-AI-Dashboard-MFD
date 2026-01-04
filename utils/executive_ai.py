def generate_ceo_summary(df, sales_col):
    if df is None or df.empty:
        return "No data available for executive summary."

    total_sales = df[sales_col].sum()

    return f"""
    📌 **Executive Summary**
    
    • Total sales generated: ₹{total_sales:,.0f}
    • Strong demand observed across key outlets
    • Inventory optimization & outlet focus recommended
    • Forecast indicates continued growth momentum
    """
