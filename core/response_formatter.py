def format_response(result):
    return {
        "header": result["title"],
        "main": result["value"],
        "explain": result["why"],
        "note": (
            "This insight is derived directly from current dataset signals "
            "and is suitable for leadership decision-making."
        )
    }
