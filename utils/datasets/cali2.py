import pandas as pd

class CaliAptPreprocessing:
    @staticmethod
    def load_and_preprocess(file_path):
        df = pd.read_csv(file_path)
        # Convert 'Time' column to datetime and rename it to 'Date'
        df['Date'] = pd.to_datetime(df['Time'], format='%m/%d/%y %H:%M')

        # Drop the old 'Time' column (optional)
        df = df.drop(columns=['Time'])
        
        df = df[['Date'] + df.select_dtypes(include=['number']).columns.tolist()]

        
        return df
