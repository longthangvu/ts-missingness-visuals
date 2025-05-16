import pandas as pd
import numpy as np
def filter_single_dataset_by_heuristics(df, features, interval='D', theta_feat=0.8, theta_joint=0.7):
    """
    Apply heuristic filtering to a single dataset.
    Returns: filtered_df, summary_df
    """
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Date'].notna()]
    df = df.set_index('Date')

    grouped = df.groupby(pd.Grouper(freq=interval))
    results = []
    metadata = []

    for name, group in grouped:
        if len(group) == 0:
            continue

        present = group[features].notna().sum()
        expected = len(group)
        feat_cov = (present / expected).fillna(0)

        if (feat_cov < theta_feat).any():
            continue

        binary = group[features].notna().astype(int)
        co_matrix = (binary.T @ binary) / expected

        i_lower = np.tril_indices(len(features), k=-1)
        if (co_matrix.values[i_lower] < theta_joint).any():
            continue

        results.append(group)
        metadata.append({
            'interval': name,
            'rows': expected,
            'min_feat_cov': feat_cov.min(),
            'min_joint_cov': co_matrix.values[i_lower].min()
        })

    filtered = pd.concat(results) if results else pd.DataFrame()
    summary = pd.DataFrame(metadata)
    return filtered.reset_index(), summary

def filter_multiple_datasets_by_heuristics(data_singleton, dataset_names, features, interval='D', theta_feat=0.8, theta_joint=0.7):
    """
    Apply heuristic filtering to multiple datasets and summarize results.

    Returns:
        results_dict: dataset_name → filtered DataFrame
        summary_df: table with rows before/after per dataset
    """
    summaries = []
    results = {}

    for name in dataset_names:
        df = data_singleton.get_data(name)
        total_rows = len(df)

        try:
            filtered, _ = filter_single_dataset_by_heuristics(
                df, features, interval, theta_feat, theta_joint
            )
            results[name] = filtered
            summaries.append({
                'dataset': name,
                'original_rows': total_rows,
                'retained_rows': len(filtered),
                'percent_retained': 100 * len(filtered) / total_rows if total_rows > 0 else 0
            })
        except Exception as e:
            summaries.append({
                'dataset': name,
                'original_rows': total_rows,
                'retained_rows': 0,
                'percent_retained': 0,
                'error': str(e)
            })

    summary_df = pd.DataFrame(summaries)
    return results, summary_df
