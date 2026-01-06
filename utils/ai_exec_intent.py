import re

MONTHS = [
    "january","february","march","april","may","june",
    "july","august","september","october","november","december"
]

def detect_intent(query: str) -> dict:
    q = query.lower()

    intent = "GENERAL"
    metric = None
    month = None

    if "sale" in q or "revenue" in q:
        metric = "sales"

    for m in MONTHS:
        if m in q:
            month = m

    if any(k in q for k in ["drop", "decline", "fall"]):
        intent = "DECLINE"
    elif "total" in q:
        intent = "TOTAL"
    elif "performance" in q:
        intent = "PERFORMANCE"
    elif "risk" in q:
        intent = "RISK"

    return {
        "intent": intent,
        "metric": metric,
        "month": month
    }
