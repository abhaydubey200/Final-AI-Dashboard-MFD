def generate_ceo_summary(kpis):
    growth = kpis["MoM Growth %"]

    if growth > 10:
        trend = "strong positive growth"
    elif growth > 0:
        trend = "moderate growth"
    else:
        trend = "decline"

    summary = f"""
    📌 **Executive Business Summary**

    The organization recorded **{trend}** in the latest month.

    • Current Month Sales: ₹{kpis['Current Month Sales']:,.0f}
    • Month-on-Month Growth: {growth}%
    • YTD Sales: ₹{kpis['YTD Sales']:,.0f}

    ⚠️ **Action Points**
    - Monitor outlets contributing to decline (if any)
    - Strengthen high-performing SKUs
    - Improve demand planning for next cycle
    """

    return summary
