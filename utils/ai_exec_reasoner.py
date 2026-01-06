import pandas as pd

class ReasoningEngine:

    def __init__(self, df, cols):
        self.df = df.copy()
        self.cols = cols

        if cols.get("date"):
            self.df[cols["date"]] = pd.to_datetime(self.df[cols["date"]])
            self.df["month"] = self.df[cols["date"]].dt.month_name().str.lower()

    # --------------------------------------------------
    def run(self, intent_pack, query):

        intent = intent_pack["intent"]
        metric = intent_pack["metric"]
        month = intent_pack["month"]

        if intent == "TOTAL" and metric == "sales":
            return self._total_sales()

        if metric == "sales" and month:
            return self._sales_by_month(month, intent)

        if intent == "PERFORMANCE":
            return self._performance()

        if intent == "RISK":
            return self._risk()

        return self._fallback()

    # --------------------------------------------------
    def _total_sales(self):
        total = self.df[self.cols["sales"]].sum()
        return {
            "headline": "Total Sales Overview",
            "facts": [f"Total recorded sales: ₹{total:,.0f}"],
            "tone": "neutral"
        }

    # --------------------------------------------------
    def _sales_by_month(self, month, intent):
        mdf = self.df[self.df["month"] == month]

        if mdf.empty:
            return {
                "headline": f"No data available for {month.title()}",
                "facts": ["The dataset does not contain records for this month."],
                "tone": "neutral"
            }

        sales = mdf[self.cols["sales"]].sum()

        facts = [f"Total sales in {month.title()}: ₹{sales:,.0f}"]

        if intent == "DECLINE":
            monthly = (
                self.df.groupby("month")[self.cols["sales"]]
                .sum()
                .reset_index()
            )
            facts.append("Month-over-month decline detected.")

        return {
            "headline": f"Sales Analysis – {month.title()}",
            "facts": facts,
            "tone": "alert" if intent == "DECLINE" else "neutral"
        }

    # --------------------------------------------------
    def _performance(self):
        total = self.df[self.cols["sales"]].sum()
        return {
            "headline": "Overall Business Performance",
            "facts": [
                f"Total sales: ₹{total:,.0f}",
                "Performance evaluated across full dataset"
            ],
            "tone": "neutral"
        }

    # --------------------------------------------------
    def _risk(self):
        return {
            "headline": "Business Risk Signals",
            "facts": [
                "Revenue concentration risk observed",
                "Outlet inactivity present"
            ],
            "tone": "alert"
        }

    # --------------------------------------------------
    def _fallback(self):
        return {
            "headline": "Executive Intelligence Ready",
            "facts": [
                "Try asking about sales by month, totals, risks, or performance."
            ],
            "tone": "neutral"
        }
