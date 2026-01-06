import pandas as pd
from utils.helpers import format_currency, safe_pct

def compute_metrics(df, intent):
    result = {}

    if intent == "TOTAL_SALES":
        total = df["AMOUNT"].sum()
        result["title"] = "📊 Total Sales Overview"
        result["value"] = format_currency(total)
        result["why"] = "Sum of AMOUNT across all orders"

    elif intent == "TOTAL_ORDERS":
        orders = df["ORDER_ID"].nunique()
        result["title"] = "📦 Total Orders"
        result["value"] = f"{orders:,}"
        result["why"] = "Unique ORDER_ID count"

    elif intent == "PERFORMANCE":
        result["title"] = "📈 Business Performance Summary"
        result["value"] = (
            f"Sales: {format_currency(df['AMOUNT'].sum())}\n"
            f"Outlets: {df['OUTLET_ID'].nunique()}\n"
            f"SKUs: {df['SKU_ID'].nunique()}"
        )
        result["why"] = "Scale, coverage and assortment indicators"

    elif intent == "SKU_ANALYSIS":
        top_brand = df.groupby("BRAND")["AMOUNT"].sum().idxmax()
        result["title"] = "🏷️ Product Performance"
        result["value"] = f"Top brand by revenue: {top_brand}"
        result["why"] = "Brand-wise revenue aggregation"

    elif intent == "OUTLET_ANALYSIS":
        inactive = df.groupby("OUTLET_ID")["ORDER_ID"].count()
        inactive = inactive[inactive <= 1].count()
        result["title"] = "🏪 Outlet Health"
        result["value"] = f"Inactive outlets detected: {inactive}"
        result["why"] = "Outlets with ≤1 order"

    elif intent == "DISCOUNT_ANALYSIS":
        discount = df["DISCOUNT_AMOUNT"].sum()
        sales = df["AMOUNT"].sum()
        result["title"] = "💸 Discount Impact"
        result["value"] = (
            f"Total Discount: {format_currency(discount)}\n"
            f"Discount % of Sales: {safe_pct(discount, sales)}%"
        )
        result["why"] = "Discount leakage assessment"

    elif intent == "REJECTION_ANALYSIS":
        rejected = df[df["ORDERSTATE"] == "Rejected"]
        result["title"] = "❌ Order Rejection Analysis"
        result["value"] = f"Rejected orders: {rejected['ORDER_ID'].nunique()}"
        result["why"] = "ORDERSTATE-based filtering"

    elif intent == "FIELD_FORCE":
        avg_time = df["TIME_SPENT_AT_OUTLET"].mean()
        result["title"] = "👥 Field Force Productivity"
        result["value"] = f"Avg time per outlet: {round(avg_time,2)} mins"
        result["why"] = "Visit efficiency proxy"

    elif intent == "RISK_ANALYSIS":
        top_share = (
            df.groupby("SKU_ID")["AMOUNT"].sum().max()
            / df["AMOUNT"].sum()
        ) * 100
        result["title"] = "⚠️ Business Risk Signals"
        result["value"] = f"Revenue concentration: {round(top_share,2)}%"
        result["why"] = "Top SKU dependency risk"

    else:
        result["title"] = "🤖 Executive Intelligence Ready"
        result["value"] = (
            "Ask about sales, orders, SKUs, outlets, risks, "
            "discounts, productivity, or geography."
        )
        result["why"] = "Dataset-supported questions only"

    return result
