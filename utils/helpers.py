def format_currency(val):
    return f"₹{val:,.0f}"

def safe_pct(a, b):
    return round((a / b) * 100, 2) if b else 0
