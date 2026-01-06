import pandas as pd

class ExecutiveStrategyEngine:
    """
    CXO-Level Strategy & Decision Engine
    Converts data → decisions → actions
    """

    def __init__(self, df, cols):
        self.df = df
        self.cols = cols

    # --------------------------------------------------
    # INTENT DETECTION
    # --------------------------------------------------
    def detect_intent(self, query: str):
        q = query.lower()

        if any(k in q for k in ["what should", "recommend", "action plan", "strategy"]):
            return "STRATEGY"

        if any(k in q for k in ["priority", "focus", "urgent"]):
            return "PRIORITY"

        if any(k in q for k in ["what if", "scenario", "impact"]):
            return "SCENARIO"

        return None

    # --------------------------------------------------
    # MAIN EXECUTOR
    # --------------------------------------------------
    def execute(self, query: str):
        intent = self.detect_intent(query)

        if intent == "STRATEGY":
            return self._strategy_actions()

        if intent == "PRIORITY":
            return self._priority_matrix()

        if intent == "SCENARIO":
            return self._scenario_analysis()

        return None

    # --------------------------------------------------
    # STRATEGY ENGINE
    # --------------------------------------------------
    def _strategy_actions(self):
        sales_col = self.cols["sales"]
        sku_col = self.cols.get("sku")
        outlet_col = self.cols.get("outlet")

        actions = []

        if sku_col:
            sku_sales = self.df.groupby(sku_col)[sales_col].sum()
            if sku_sales.max() / sku_sales.sum() > 0.40:
                actions.append("Reduce over-dependence on top SKU by scaling secondary SKUs")

        if outlet_col:
            outlet_sales = self.df.groupby(outlet_col)[sales_col].sum()
            low_perf = (outlet_sales < outlet_sales.mean()).sum()
            if low_perf > 0:
                actions.append("Launch outlet reactivation & incentive programs")

        actions.append("Strengthen distributor execution & stock visibility")
        actions.append("Increase leadership review cadence for next 60 days")

        bullets = "\n".join([f"{i+1}. {a}" for i, a in enumerate(actions)])

        return f"""
## 🎯 Executive Strategy Recommendations

**Immediate Actions**
{bullets}

**Execution Horizon**
• Tactical impact: 30 days  
• Strategic impact: 60–90 days  

**Risk of Inaction**
Sustained revenue leakage and execution inefficiency.
"""

    # --------------------------------------------------
    # PRIORITY MATRIX
    # --------------------------------------------------
    def _priority_matrix(self):
        return """
## 🔥 Leadership Priority Matrix

### HIGH PRIORITY
• SKU concentration risk  
• Outlet churn risk  
• Distribution execution gaps  

### MEDIUM PRIORITY
• Pricing optimization  
• Regional performance imbalance  

### LOW PRIORITY
• Long-tail SKU rationalization  

**CEO Directive**
Close HIGH priorities within 30 days.
"""

    # --------------------------------------------------
    # SCENARIO ENGINE
    # --------------------------------------------------
    def _scenario_analysis(self):
        sales_col = self.cols["sales"]
        total_sales = self.df[sales_col].sum()
        impact = total_sales * 0.10

        return f"""
## 📉 Scenario Analysis: 10% Sales Decline

**Estimated Revenue Impact**
₹{impact:,.0f}

**Probable Causes**
• Distribution leakage  
• Demand slowdown  
• SKU fatigue  

**Mitigation Plan**
• Tactical trade schemes  
• Focused SKU push  
• Outlet-level incentives  

**Decision Urgency**: HIGH
"""
