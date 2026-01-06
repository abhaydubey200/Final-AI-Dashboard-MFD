def detect_intent(query: str) -> str:
    q = query.lower()

    if any(k in q for k in ["trend", "performance", "growth", "decline"]):
        return "PERFORMANCE"

    if any(k in q for k in ["risk", "problem", "issue", "drop"]):
        return "RISK"

    if any(k in q for k in ["why", "cause", "reason"]):
        return "DIAGNOSIS"

    if any(k in q for k in ["what should", "recommend", "strategy", "action"]):
        return "STRATEGY"

    if any(k in q for k in ["priority", "focus", "urgent"]):
        return "PRIORITY"

    if any(k in q for k in ["what if", "scenario", "impact"]):
        return "SCENARIO"

    return "GENERAL"
