def outlet_risk_score(churn_df):
    if churn_df.empty:
        return churn_df

    score_map = {"Low": 1, "Medium": 2, "High": 3}
    churn_df["Risk_Score"] = churn_df["Churn_Risk"].map(score_map)

    return churn_df
