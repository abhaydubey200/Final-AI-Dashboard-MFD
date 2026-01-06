def priority_badge(level: str) -> str:
    if level == "High":
        return "🔴 HIGH PRIORITY"
    if level == "Medium":
        return "🟡 MEDIUM PRIORITY"
    return "🟢 LOW PRIORITY"
