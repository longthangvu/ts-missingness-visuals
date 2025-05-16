import plotly.graph_objects as go
import numpy as np
import pandas as pd

def plot_time_series_heatmap(df: pd.DataFrame, title: str = "Time Series Heatmap") -> go.Figure:
    """
    Create a heatmap of feature values over time.

    Parameters:
        df (pd.DataFrame): Must include a 'Date' column and numeric columns.
        title (str): Plot title.

    Returns:
        go.Figure: A Plotly heatmap object (not shown).
    """
    if 'Date' not in df.columns:
        raise ValueError("DataFrame must include a 'Date' column.")
    
    df = df.copy().sort_values('Date')
    df = df.set_index('Date')
    numeric_cols = df.select_dtypes(include='number').columns

    fig = go.Figure(data=go.Heatmap(
        z=df[numeric_cols].T.values,  # shape (features, time)
        x=df.index,                   # time axis
        y=numeric_cols,              # feature names
        colorscale='Viridis',
        colorbar=dict(title='Value')
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Feature",
        height=400 + 20 * len(numeric_cols),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig

def plot_temporal_coverage_heatmap(df: pd.DataFrame, sample_rate='D', selected_columns=None, title=None) -> go.Figure:
    """
    Plot a temporal coverage heatmap using nested resampling logic.

    Parameters:
        df (pd.DataFrame): Must include a 'Date' column and numeric columns.
        sample_rate (str): Target bin size ('D', 'W', 'M', etc.)
        selected_columns (list or None): Optional subset of columns.
        title (str): Optional plot title.

    Returns:
        go.Figure: A Plotly heatmap object.
    """
    TIME_RANGE_TO_RATE = {'D': 'h', 'W': 'h', 'M': 'D', 'H': 'min', 'min': 's'}

    try:
        if 'Date' not in df.columns:
            raise ValueError("DataFrame must include a 'Date' column.")

        if sample_rate not in TIME_RANGE_TO_RATE:
            raise ValueError(f"Unsupported sample_rate: {sample_rate}")

        finer_rate = TIME_RANGE_TO_RATE[sample_rate]

        df = df.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')

        finer = df.set_index('Date').resample(finer_rate).mean().reset_index()

        if finer.empty:
            raise ValueError("No data after finer resampling")

        # Generate broader bins
        if sample_rate == 'M':
            broader_bins = pd.date_range(start=finer['Date'].iloc[0], end=finer['Date'].iloc[-1], freq='MS')
        else:
            broader_bins = pd.date_range(start=finer['Date'].iloc[0], end=finer['Date'].iloc[-1], freq=sample_rate)

        if len(broader_bins) < 2:
            raise ValueError("Not enough intervals to compute heatmap")

        if not selected_columns:
            selected_columns = list(finer.columns)
            selected_columns.remove('Date')

        coverage_matrix = []

        for col in selected_columns:
            finer['bin'] = pd.cut(finer['Date'], bins=broader_bins, labels=broader_bins[:-1], right=False)
            bin_counts = finer.groupby('bin', observed=True)[col].count()

            broader_dur = pd.Timedelta(f'1{sample_rate}')
            finer_dur = pd.Timedelta(f'1{finer_rate}')
            max_points = max(broader_dur.total_seconds() / finer_dur.total_seconds(), 1)

            coverage = (bin_counts / max_points) * 100
            coverage = coverage.reindex(broader_bins[:-1], fill_value=0).tolist()
            coverage_matrix.append(coverage)

        time_labels = [str(t) for t in broader_bins[:-1]]
        fig = go.Figure(data=go.Heatmap(
            z=coverage_matrix,
            x=time_labels,
            y=selected_columns,
            colorscale='Blues',
            zmin=0,
            zmax=100,
            colorbar=dict(title="Coverage (%)")
        ))

        fig.update_layout(
            title=title or f"Temporal Coverage Heatmap ({sample_rate} bins)",
            xaxis_title="Time Intervals",
            yaxis_title="Features",
            margin=dict(l=40, r=40, t=40, b=40),
            height=400 + 20 * len(selected_columns),
        )
        return fig

    except Exception as e:
        fig = go.Figure()
        fig.update_layout(
            title=f"Error: {str(e)}",
            margin=dict(l=40, r=40, t=40, b=40),
        )
        return fig