def detect_column(columns, keywords):
    """
    Detect first matching column based on keyword priority.
    Case-insensitive, safe for production.
    """
    if columns is None:
        return None

    for key in keywords:
        for col in columns:
            try:
                if key in col.lower():
                    return col
            except Exception:
                continue

    return None


def auto_detect_columns(df):
    """
    Auto-detect commonly used business columns.
    Returns a dictionary used across ALL dashboards.
    """

    if df is None or df.empty:
        return {
            "date": None,
            "sales": None,
            "quantity": None,
            "sku": None,
            "brand": None,
            "city": None,
            "state": None,
            "outlet": None,
            "rep": None
        }

    cols = df.columns.tolist()

    return {
        # Date
        "date": detect_column(
            cols,
            ["order_date", "date", "created_date", "invoice_date"]
        ),

        # Sales / Revenue
        "sales": detect_column(
            cols,
            ["amount", "sales", "sales_value", "net_amount", "value"]
        ),

        # Quantity
        "quantity": detect_column(
            cols,
            ["total_quantity", "quantity", "qty", "units"]
        ),

        # SKU / Product
        "sku": detect_column(
            cols,
            ["sku", "product_code", "product", "item"]
        ),

        # Brand
        "brand": detect_column(
            cols,
            ["brand"]
        ),

        # City
        "city": detect_column(
            cols,
            ["city", "town"]
        ),

        # State
        "state": detect_column(
            cols,
            ["state", "region"]
        ),

        # Outlet / Store
        "outlet": detect_column(
            cols,
            ["outlet", "store", "retailer", "shop"]
        ),

        # Sales Representative
        "rep": detect_column(
            cols,
            ["sales_rep", "rep", "salesman", "user", "executive"]
        )
    }
