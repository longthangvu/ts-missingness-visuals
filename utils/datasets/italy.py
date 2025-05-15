import pandas as pd

class ItalyPreprocessing:
    @staticmethod
    def load_and_preprocess(file_path):
        df = pd.read_csv(file_path, low_memory=False, delimiter=';')
    
        df['ts_insertion'] = pd.to_datetime(df['ts_insertion'], format='%Y-%m-%d %H:%M:%S')
        
        df = df.rename(columns={'ts_insertion': 'Date'})
        
        return df
