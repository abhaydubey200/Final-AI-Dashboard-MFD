class ResponseComposer:
    """
    Converts structured reasoning → human executive response
    """

    def compose(self, intent, payload):
        headline = payload["headline"]
        facts = payload["facts"]
        tone = payload["tone"]

        icon = {
            "neutral": "📊",
            "alert": "⚠️",
            "analytical": "🧠",
            "directive": "🎯",
            "urgent": "🔥",
            "critical": "🚨"
        }.get(tone, "📌")

        bullets = "\n".join([f"- {f}" for f in facts])

        return f"""
### {icon} {headline}

{bullets}

**Executive Note**  
This insight is derived directly from current dataset signals and is suitable for leadership decision-making.
"""
