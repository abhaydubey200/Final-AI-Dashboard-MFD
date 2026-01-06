def detect_intent(query: str):
    q = query.lower()

    if "total sales" in q or "revenue" in q:
        return "TOTAL_SALES"

    if "orders" in q:
        return "TOTAL_ORDERS"

    if "performance" in q:
        return "PERFORMANCE"

    if "sku" in q or "brand" in q:
        return "SKU_ANALYSIS"

    if "outlet" in q:
        return "OUTLET_ANALYSIS"

    if "zone" in q or "state" in q or "city" in q:
        return "GEO_ANALYSIS"

    if "discount" in q:
        return "DISCOUNT_ANALYSIS"

    if "rejected" in q or "rejection" in q:
        return "REJECTION_ANALYSIS"

    if "productivity" in q or "employee" in q:
        return "FIELD_FORCE"

    if "risk" in q or "drop" in q:
        return "RISK_ANALYSIS"

    return "HELP"
