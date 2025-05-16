import pandas as pd
import numpy as np

def compute_partial_co_coverage_vector(df, feature_pool, daily_bins):
    """
    Compute average co-coverage vector for a dataset using only available features.
    Missing features are zero-padded later.

    Parameters:
        df (pd.DataFrame): Dataset with 'Date' and candidate features.
        feature_pool (list): Full list of target features across datasets.
        daily_bins (pd.DatetimeIndex): Daily time bins.

    Returns:
        list: Average co-coverage for each feature in feature_pool (zero if not in dataset).
    """
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df[df['Date'].notna()]
    df = df[df['Date'].between(daily_bins[0], daily_bins[-1])]

    available = [f for f in feature_pool if f in df.columns]
    if len(available) < 1:
        return None

    df['bin'] = pd.cut(df['Date'], bins=daily_bins, labels=daily_bins[:-1], right=False)

    daily_presence = pd.DataFrame(0, index=daily_bins[:-1], columns=available)
    for col in available:
        daily_presence[col] = df.groupby('bin', observed=True)[col].apply(lambda x: x.notna().any()).astype(int)

    T = len(daily_bins) - 1
    co_matrix = pd.DataFrame(0.0, index=available, columns=available)
    for i in available:
        for j in available:
            # co_matrix.loc[i, j] = (daily_presence[i] & daily_presence[j]).sum() / T
            co_matrix.loc[i, j] = (daily_presence[i].astype(bool) & daily_presence[j].astype(bool)).sum() / T
    avg_cov = co_matrix.mean(axis=1)
    return [avg_cov.get(f, 0.0) for f in feature_pool]

def compute_avg_daily_co_coverage_vector(df, features, daily_bins):
    """
    Compute average daily co-coverage vector for a single dataset.

    Parameters:
        df (pd.DataFrame): Dataset with 'Date' and pollutant columns.
        features (list): Features to analyze.
        daily_bins (pd.DatetimeIndex): Bins for daily intervals.

    Returns:
        list: Average co-coverage per feature.
    """
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df[df['Date'].notna()]
    df = df[df['Date'].between(daily_bins[0], daily_bins[-1])]

    available = [col for col in features if col in df.columns]
    if len(available) < 2:
        return None

    df['bin'] = pd.cut(df['Date'], bins=daily_bins, labels=daily_bins[:-1], right=False)

    daily_presence = pd.DataFrame(0, index=daily_bins[:-1], columns=available)
    for col in available:
        daily_presence[col] = df.groupby('bin', observed=True)[col].apply(lambda x: x.notna().any()).astype(int)

    T = len(daily_bins) - 1
    co_matrix = pd.DataFrame(0.0, index=available, columns=available)
    for i in available:
        for j in available:
            co_matrix.loc[i, j] = (daily_presence[i].astype(bool) & daily_presence[j].astype(bool)).sum() / T

    avg_vector = [co_matrix[feature].mean() if feature in co_matrix else 0 for feature in features]
    return avg_vector


def compute_co_coverage_matrix(df: pd.DataFrame, selected_columns=None) -> pd.DataFrame:
    """
    Compute the co-coverage matrix for a given DataFrame.

    Parameters:
        df (pd.DataFrame): Must include 'Date' and numeric columns.
        selected_columns (list or None): Optional subset of columns to include.

    Returns:
        pd.DataFrame: Symmetric matrix of co-coverage percentages (0-100).
    """
    if 'Date' not in df.columns:
        raise ValueError("DataFrame must include a 'Date' column.")

    df = df.copy()
    df = df.set_index('Date')

    numeric_cols = df.select_dtypes(include='number').columns
    if selected_columns:
        numeric_cols = [col for col in selected_columns if col in numeric_cols]

    presence = df[numeric_cols].notna().astype(int)  # binary matrix

    co_counts = presence.T @ presence         # shared timestamps
    total_counts = presence.shape[0]          # total time points

    co_coverage = co_counts / total_counts * 100  # as percent
    return co_coverage

if __name__ == "__main__":
    # Example usage
    df = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=100, freq='H'),
        'Feature1': np.random.rand(100),
        'Feature2': np.random.rand(100),
        'Feature3': np.random.rand(100)
    })
    df.loc[10:20, 'Feature2'] = np.nan  # introduce some missing values

    co_coverage_matrix = compute_co_coverage_matrix(df)
    print(co_coverage_matrix)
    print(co_coverage_matrix.columns)