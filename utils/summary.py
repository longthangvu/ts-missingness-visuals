import pandas as pd

def calculate_comprehensive_statistics(data_singleton, resolution='D', finer_resolution='h', threshold=0.8, debug=False):
    """
    Compute comprehensive statistics for each dataset, ensuring:
    - More accurate recorded data percentage
    - Stricter criteria for recorded bins (requiring at least 50% of hours)
    - Total expected bins remain all possible days
    
    Args:
        data_singleton: The DataSingleton object containing datasets.
        resolution (str): Temporal resolution for aggregation (e.g., 'D' for daily).
        finer_resolution (str): Finer resolution for checking data presence (e.g., 'H' for hourly).
        threshold (float): Minimum percentage of expected data per bin to be considered usable.
        debug (bool): Whether to print debug information for detailed analysis.

    Returns:
        pd.DataFrame: A DataFrame containing comprehensive statistics for each dataset.
    """
    stats = {}
    prefixes = ['Sweden', 'Italy', 'Caliapt', 'Calihome']
    aggregated_datasets = {prefix: [] for prefix in prefixes}
    non_grouped_datasets = {}
    
    # Group datasets by prefix
    for dataset_name in data_singleton._data_store:
        matched = False
        for prefix in prefixes:
            if dataset_name.startswith(prefix):
                aggregated_datasets[prefix].append(dataset_name)
                matched = True
                break
        if not matched:
            non_grouped_datasets[dataset_name] = dataset_name
    
    def compute_stats(data, dataset_name):
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        data = data.dropna(subset=['Date'])  # Ensure no missing dates
        data.set_index('Date', inplace=True)  # Set Date as index
        total_records = len(data)
        
        # Identify missing timestamps
        missing_records = data.isnull().sum().sum()
        completeness_ratio = (total_records - missing_records) / total_records if total_records > 0 else 0
        
        # Determine time span covered
        time_span = (data.index.max() - data.index.min()).days
        
        # Resample to finer resolution and check data presence
        finer_resampled_data = data.resample(finer_resolution).size()
        finer_resampled_data = finer_resampled_data > 0
        finer_resampled_data = finer_resampled_data.astype(int)

        # Group by daily bins properly using pd.Grouper
        daily_counts = finer_resampled_data.groupby(pd.Grouper(freq=resolution)).sum()
        
        total_expected_bins = len(daily_counts)
        recorded_bins = (daily_counts >= 12).sum()  # Require at least 12 hours in a day
        usable_bins = (daily_counts / 24 >= threshold).sum()
        usable_bins2 = (daily_counts / 24 >= 0.5).sum()
        
        
        if debug and dataset_name.startswith("Sweden"):
            print(f"\nDebugging {dataset_name}:")
            print(f"Total Expected Bins (All Days): {total_expected_bins}")
            print(f"Recorded Bins (>=12 hours/day): {recorded_bins}")
            print(f"Usable Bins (>80% data): {usable_bins}")
            print(f"Total Records: {total_records}")
            print(f"Missing Records: {missing_records}")
            print(f"Completeness Ratio: {completeness_ratio * 100:.2f}%")
            print(f"Time Span Covered (Days): {time_span}")
            print("Sample of Daily Bin Counts:")
            print(daily_counts.sample(10))  # Print 10 random daily bin counts for validation
        
        return {
            'Total Records': total_records,
            'Missing Records': missing_records,
            'Completeness Ratio': completeness_ratio * 100,
            'Time Span (days)': time_span,
            'Total Expected Bins': total_expected_bins,
            'Recorded Bins (>=12h)': recorded_bins,
            'Usable Bins (>80%)': usable_bins,
            'Percentage Recorded Data': (recorded_bins / total_expected_bins) * 100 if total_expected_bins > 0 else 0,
            'Percentage Usable Data (>80%)': (usable_bins / total_expected_bins) * 100 if total_expected_bins > 0 else 0,
            'Percentage Usable Data (>50%)': (usable_bins2 / total_expected_bins) * 100 if total_expected_bins > 0 else 0
        }
    
    # Process grouped datasets by averaging sub-dataset statistics
    for group, dataset_names in aggregated_datasets.items():
        if dataset_names:
            sub_stats = [compute_stats(data_singleton.get_data(name), name) for name in dataset_names]
            stats[group] = {metric: sum(d[metric] for d in sub_stats) / len(sub_stats) for metric in sub_stats[0]}
    
    # Process non-grouped datasets individually
    for dataset_name in non_grouped_datasets:
        stats[dataset_name] = compute_stats(data_singleton.get_data(dataset_name), dataset_name)
    
    return pd.DataFrame.from_dict(stats, orient='index')