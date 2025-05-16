import pandas as pd
import numpy as np

def compute_gap_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute missing gap statistics for each numeric feature.

    Returns:
        DataFrame with columns: feature, num_gaps, mean_gap, max_gap
    """
    if 'Date' not in df.columns:
        raise ValueError("DataFrame must include a 'Date' column.")

    df = df.copy().sort_values('Date')
    stats = []

    for col in df.select_dtypes(include='number').columns:
        is_na = df[col].isna()
        gaps = (is_na != is_na.shift()).cumsum()[is_na]  # group consecutive NaNs
        gap_lengths = gaps.value_counts().values

        if len(gap_lengths) > 0:
            stats.append({
                'feature': col,
                'num_gaps': len(gap_lengths),
                'mean_gap': np.mean(gap_lengths),
                'max_gap': np.max(gap_lengths)
            })
        else:
            stats.append({
                'feature': col,
                'num_gaps': 0,
                'mean_gap': 0,
                'max_gap': 0
            })

    return pd.DataFrame(stats)


def compute_feature_coverage(df: pd.DataFrame) -> pd.Series:
    """
    Compute the percentage of non-missing values for each numeric column.

    Returns:
        Series with feature names and % of available data.
    """
    numeric_cols = df.select_dtypes(include='number').columns
    total = len(df)
    return df[numeric_cols].notna().sum() / total * 100


def compute_periodic_coverage(df: pd.DataFrame, freq='D') -> pd.DataFrame:
    """
    Compute per-period (e.g., per day) coverage for each feature.

    Returns:
        DataFrame: rows = periods, columns = features, values = % coverage
    """
    if 'Date' not in df.columns:
        raise ValueError("DataFrame must include a 'Date' column.")

    df = df.copy().sort_values('Date').set_index('Date')
    numeric_cols = df.select_dtypes(include='number').columns

    grouped = df[numeric_cols].groupby(pd.Grouper(freq=freq))
    counts = grouped.count()
    total_per_period = grouped.size().replace(0, np.nan)

    return counts.div(total_per_period, axis=0) * 100

def reconstruct_time_index(df: pd.DataFrame, inferred_freq: str = None) -> pd.DataFrame:
    """
    Reindex the time series DataFrame onto a full DateTimeIndex at inferred or given frequency.

    Parameters:
        df (pd.DataFrame): Must include a 'Date' column.
        inferred_freq (str or None): If None, will auto-infer the frequency.

    Returns:
        pd.DataFrame: Reindexed DataFrame with missing rows filled as NaN.
    """
    if 'Date' not in df.columns:
        raise ValueError("DataFrame must include a 'Date' column.")
    
    df = df.copy().sort_values('Date')
    df = df.set_index('Date')

    if inferred_freq is None:
        inferred_freq = pd.infer_freq(df.index[:100])
        if inferred_freq is None:
            raise ValueError("Could not infer frequency. Please specify it manually.")

    full_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq=inferred_freq)
    df = df.reindex(full_index)

    df.index.name = 'Date'
    return df.reset_index()

if __name__ == "__main__":
    # Example usage
    df = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=100, freq='H'),
        'Value1': range(100),
        'Value2': [np.nan if i % 10 == 0 else i for i in range(100)]
    })

    gap_stats = compute_gap_stats(df)
    print(gap_stats)

    coverage = compute_feature_coverage(df)
    print(coverage)

    periodic_coverage = compute_periodic_coverage(df, freq='D')
    print(periodic_coverage)

    reindexed_df = reconstruct_time_index(df)
    print(reindexed_df.head())