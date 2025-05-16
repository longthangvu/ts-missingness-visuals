# ts-missingness-visuals

A Python toolkit for visualizing and analyzing missingness in time series datasets, with a focus on environmental sensor data.

## Features
- Visualize temporal coverage and missing data patterns
- Compute and plot co-coverage between features and datasets
- Resample and preprocess time series data
- Gap statistics and missingness analysis
- Interactive visualizations using Plotly

## Project Structure
- `utils/` — Core modules for data loading, processing, and visualization
  - `get_data.py` — Data loading utilities
  - `helper_functions.py` — Time series resampling, gap stats, and helpers
  - `co_coverage.py` — Co-coverage computation
  - `plot_functions.py` — Plotly-based visualization functions
  - `missingness.py` — Missingness and gap analysis
  - `datasets/` — Example datasets (India, Sweden, etc.)
- `summary.ipynb` — Example notebook for summary analysis
- `test.ipynb` — Notebook for testing and exploration

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/longthangvu/ts-missingness-visuals
   cd ts-missingness-visuals
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
Open the notebooks (`summary.ipynb`) in VS Code or Jupyter Lab. Run the cells to load data, analyze missingness, and generate visualizations.

## Example
```python
from utils.get_data import get_data
from utils.helper_functions import resample_time_series
from utils.plot_functions import plot_time_series_heatmap

data_singleton = get_data()
india_df = data_singleton.get_data('India')
df_daily = resample_time_series(india_df, freq='d')
plot_time_series_heatmap(df_daily).show()
```

## Requirements
- Python 3.8+
- pandas, numpy, plotly, jupyter, etc. (see `requirements.txt`)

## License
MIT License
