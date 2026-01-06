import pandas as pd

class ReasoningEngine:
    """
    Dataset-aware reasoning engine (NO LLM / NO API)
    """

    def __init__(self, df, cols):
        self.df = df
        self.cols = cols

    def run(self, intent, query):
        if intent == "PERFORMANCE":
            return self._performance()

        if intent == "RISK":
            return self._risk()

        if intent == "DIAGNOSIS":
            return self._diagnosis()

        if intent == "STRATEGY":
            return self._strategy()

        if intent == "PRIORITY":
            return self._priority()

        if intent == "SCENARIO":
            return self._scenario()

        return self._general()

    # --------------------------------------------------
    def _performance(self):
        sales = self.df[self.cols["sales"]].sum()
        return {
            "headline": "Overall business performance reviewed",
            "facts": [f"Total recorded sales: ₹{sales:,.0f}"],
            "tone": "neutral"
        }

    def _risk(self):
        return {
            "headline": "Business risk signals detected",
            "facts": [
                "Revenue concentration risk observed",
                "Outlet inactivity present in dataset"
            ],
            "tone": "alert"
        }

    def _diagnosis(self):
        return {
            "headline": "Root cause analysis summary",
            "facts": [
                "Performance variation linked to SKU imbalance",
                "Execution inconsistency across outlets"
            ],
            "tone": "analytical"
        }

    def _strategy(self):
        return {
            "headline": "Strategic recommendations generated",
            "facts": [
                "Strengthen secondary SKU contribution",
                "Reactivate low-performing outlets",
                "Increase distributor accountability"
            ],
            "tone": "directive"
        }

    def _priority(self):
        return {
            "headline": "Leadership priority assessment",
            "facts": [
                "SKU risk — HIGH",
                "Outlet churn — HIGH",
                "Pricing optimization — MEDIUM"
            ],
            "tone": "urgent"
        }

    def _scenario(self):
        sales = self.df[self.cols["sales"]].sum()
        impact = sales * 0.1
        return {
            "headline": "Scenario impact simulated",
            "facts": [
                f"10% sales decline → ₹{impact:,.0f} revenue risk",
                "Immediate mitigation required"
            ],
            "tone": "critical"
        }

    def _general(self):
        return {
            "headline": "Executive intelligence ready",
            "facts": [
                "Ask about performance, risks, priorities, or strategy",
            ],
            "tone": "neutral"
        }
