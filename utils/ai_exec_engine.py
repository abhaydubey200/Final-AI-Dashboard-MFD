import pandas as pd
import numpy as np
import re

class ExecutiveAIEngine:
    """
    Deterministic AI Reasoning Engine (API-Free)
    Enterprise Safe | CXO Grade
    """

    def __init__(self, df, cols):
        self.df = df.copy()
        self.cols = cols

        if self.cols.get("date"):
            self.df[self.cols["date"]] = pd.to_datetime(self.df[self.cols["date"]])

    # -----------------------------
    # Intent Detection
    # -----------------------------
    def detect_intent(self, query: str):
        q = query.lower()

        if any(k in q for k in ["total", "sum", "overall"]):
            return "TOTAL"

        if any(k in q for k in ["average", "avg", "mean"]):
            return "AVERAGE"

        if any(k in q for k in ["top", "highest", "best"]):
            return "TOP"

        if any(k in q for k in ["count", "how many", "number of"]):
            return "COUNT"

        if any(k in q for k in ["trend", "growth"]):
            return "TREND"

        return "UNKNOWN"

    # -----------------------------
    # Query Execution
    # -----------------------------
    def execute(self, query: str):
        intent = self.detect_intent(query)

        if intent == "TOTAL":
            return self._total_sales()

        if intent == "AVERAGE":
            return self._average_sales()

        if intent == "TOP":
            return self._top_entities(query)

        if intent == "COUNT":
            return self._count_entities(query)

        return self._fallback()

    # -----------------------------
    # Handlers
    # -----------------------------
    def _total_sales(self):
        sales_col = self.cols.get("sales")
        total = self.df[sales_col].sum()

        return f"""
**Executive Summary**

Total business sales stand at **₹{total:,.0f}**.

This figure represents cumulative sales across the complete uploaded dataset.
"""

    def _average_sales(self):
        sales_col = self.cols.get("sales")
        avg = self.df[sales_col].mean()

        return f"""
**Executive Summary**

The average sales value is **₹{avg:,.0f}** per transaction.

This metric reflects typical transaction performance.
"""

    def _top_entities(self, query):
        sales_col = self.cols.get("sales")

        if "sku" in query and self.cols.get("sku"):
            g = self.df.groupby(self.cols["sku"])[sales_col].sum().sort_values(ascending=False)
            top = g.head(5)

            text = "\n".join([f"- {k}: ₹{v:,.0f}" for k, v in top.items()])
            return f"""
**Top Performing SKUs**

{text}
"""

        if "outlet" in query and self.cols.get("outlet"):
            g = self.df.groupby(self.cols["outlet"])[sales_col].sum().sort_values(ascending=False)
            top = g.head(5)

            text = "\n".join([f"- {k}: ₹{v:,.0f}" for k, v in top.items()])
            return f"""
**Top Performing Outlets**

{text}
"""

        return self._fallback()

    def _count_entities(self, query):
        if "outlet" in query and self.cols.get("outlet"):
            count = self.df[self.cols["outlet"]].nunique()
            return f"Total active outlets in dataset: **{count}**"

        if "sku" in query and self.cols.get("sku"):
            count = self.df[self.cols["sku"]].nunique()
            return f"Total SKUs in dataset: **{count}**"

        return self._fallback()

    def _fallback(self):
        return """
I am currently optimized for **numeric, KPI-based executive questions**.

Examples:
• Total sales  
• Top 5 SKUs  
• Number of outlets  
• Average sales  

Advanced reasoning will be enabled in next upgrade.
"""
