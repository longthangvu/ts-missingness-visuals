# preprocessing/india_preprocessing.py
import pandas as pd

class IndiaPreprocessing:
    @staticmethod
    def load_and_preprocess(file_path):
        # Example loading with potential India-specific column names and formats
        df = pd.read_csv(file_path, low_memory=False)

        df.iloc[:, :8] = df.iloc[:, :8].apply(pd.to_numeric, errors='raise')
        df['Date'] = pd.to_datetime(df['Date'].str.replace('|', ' '), format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
        df = df.iloc[:, :9]
        return df
