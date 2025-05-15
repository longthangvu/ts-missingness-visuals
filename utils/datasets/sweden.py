import pandas as pd

class SwedenPreprocessing:
    @staticmethod
    def load_and_preprocess(file_path):
        # Load the file
        df = pd.read_csv(file_path, delimiter='\t')
        
        # Rename columns from Swedish to English
        df.columns = ['Date', 'Temperature', 'Humidity', 'CO2', 'PM1', 'PM2.5', 'PM10']
        
        # Parse the Date column
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M')
        
        # Convert other columns to numeric, handling commas as decimal points
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
        
        return df
