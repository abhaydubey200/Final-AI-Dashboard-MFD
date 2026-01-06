def build_reasoned_response(signal: dict) -> str:
    """
    Converts a raw signal into CEO-style reasoning.
    """

    return f"""
### {signal['signal']}
**Priority:** {signal['priority']}

**What is happening**
• {signal['signal']}

**Why this matters**
• {signal['reason']}

**What leadership should do**
• {signal['action']}
"""
