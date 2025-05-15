import pandas as pd

class CaliPreprocessing:
    @staticmethod
    def load_and_preprocess(file_path):
        df = pd.read_csv(file_path)
    
        # Rename the 'Time' column to 'Date'
        df = df.rename(columns={'Time': 'Date'})
        
        # Convert 'Date' to datetime format
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        
        df = df[['Date'] + df.select_dtypes(include=['number']).columns.tolist()]

        
        return df
