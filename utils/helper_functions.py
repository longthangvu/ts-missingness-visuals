import pandas as pd

def resample_time_series(df, freq='D', agg='mean'):
    """
    Resample a time series DataFrame to a specified frequency.

    Parameters:
        df (pd.DataFrame): Must include a 'Date' column in datetime format.
        freq (str): Resample frequency string (e.g., 'D', 'H', 'M', 'W').
        agg (str): Aggregation method: 'mean', 'sum', etc.

    Returns:
        pd.DataFrame: Resampled DataFrame with 'Date' column.
    """
    if 'Date' not in df.columns:
        raise ValueError("DataFrame must include a 'Date' column.")
    
    df = df.copy()
    df = df.set_index('Date')
    
    if agg == 'mean':
        df_resampled = df.resample(freq).mean()
    elif agg == 'sum':
        df_resampled = df.resample(freq).sum()
    else:
        raise ValueError(f"Unsupported aggregation: {agg}")
    
    df_resampled = df_resampled.reset_index()
    return df_resampled

def get_expected_points_per_interval(original_df, target_freq='D'):
    """
    Estimate the number of expected samples per interval after resampling.

    Parameters:
        original_df (pd.DataFrame): Original time series with 'Date'.
        target_freq (str): Target resample frequency ('D', 'H', 'M', 'W').

    Returns:
        int: Expected number of points per interval.
    """
    if 'Date' not in original_df.columns:
        raise ValueError("DataFrame must include a 'Date' column.")

    df = original_df.sort_values('Date').copy()
    time_deltas = df['Date'].diff().dropna()

    if len(time_deltas) == 0:
        return 1  # default fallback if no deltas available

    median_delta = time_deltas.median()

    # Compute expected number of points based on time delta
    interval_length = {
        'D': pd.Timedelta(days=1),
        'h': pd.Timedelta(hours=1),
        'M': pd.Timedelta(minutes=1),
        'W': pd.Timedelta(weeks=1)
    }.get(target_freq)

    if interval_length is None:
        raise ValueError(f"Unsupported target frequency: {target_freq}")

    expected = int(interval_length / median_delta)
    return expected

from utils.co_coverage import compute_partial_co_coverage_vector
import pandas as pd

def gather_cross_dataset_co_coverage(data_singleton, dataset_names, start_date, end_date, feature_pool):
    """
    Collect partial co-coverage vectors (zero-padded) for selected datasets.

    Returns:
        vectors (list of list of float)
        successful_names (list of str)
    """
    daily_bins = pd.date_range(start=start_date, end=end_date, freq='D')
    vectors = []
    names = []

    for name in dataset_names:
        try:
            df = data_singleton.get_data(name)
            vec = compute_partial_co_coverage_vector(df, feature_pool, daily_bins)
            if vec is not None:
                vectors.append(vec)
                names.append(name)
        except Exception as e:
            print(f"Skipping {name}: {e}")
    return vectors, names

if __name__ == "__main__":
    # Example usage
    df = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=100, freq='H'),
        'Value': range(100)
    })
    
    resampled_df = resample_time_series(df, freq='D', agg='mean')
    print(resampled_df.head())
    
    expected_points = get_expected_points_per_interval(df, target_freq='D')
    print(f"Expected points per day: {expected_points}")