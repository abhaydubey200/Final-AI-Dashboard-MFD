import numpy as np
import pandas as pd

def detect_business_signals(df: pd.DataFrame, numeric_cols: list):
    """
    Detects volatility-based business risks & opportunities.
    Returns CEO-grade signals with priority, reason, and action.
    """

    signals = []

    for col in numeric_cols:
        series = df[col].dropna()

        if series.empty or series.mean() == 0:
            continue

        volatility = series.std() / abs(series.mean())

        if volatility >= 0.8:
            signals.append({
                "metric": col,
                "priority": "High",
                "signal": f"Severe instability detected in {col}",
                "reason": "Extreme fluctuations indicate execution or demand breakdown",
                "action": "Immediate leadership review and corrective intervention required"
            })

        elif volatility >= 0.4:
            signals.append({
                "metric": col,
                "priority": "Medium",
                "signal": f"Inconsistent performance observed in {col}",
                "reason": "Performance variability impacting predictability",
                "action": "Operational optimization and monitoring advised"
            })

        else:
            signals.append({
                "metric": col,
                "priority": "Low",
                "signal": f"Stable trend observed in {col}",
                "reason": "Metric performance within acceptable variance",
                "action": "Maintain current execution strategy"
            })

    return signals
