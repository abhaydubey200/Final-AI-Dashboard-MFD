import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def prepare_outlet_features(df, outlet_col, sales_col, qty_col):
    if df is None or df.empty:
        return pd.DataFrame()

    if outlet_col not in df.columns:
        return pd.DataFrame()

    agg = {}
    if sales_col in df.columns:
        agg[sales_col] = "sum"
    if qty_col in df.columns:
        agg[qty_col] = "sum"

    outlet_df = df.groupby(outlet_col, as_index=False).agg(agg)
    outlet_df.fillna(0, inplace=True)

    return outlet_df


def segment_outlets(outlet_df, n_clusters=3):
    if outlet_df is None or outlet_df.empty:
        return pd.DataFrame()

    features = outlet_df.select_dtypes(include="number")
    if features.empty or len(outlet_df) < n_clusters:
        outlet_df["Segment"] = "Single Cluster"
        return outlet_df

    scaler = StandardScaler()
    X = scaler.fit_transform(features)

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    outlet_df["Segment"] = model.fit_predict(X)

    return outlet_df
