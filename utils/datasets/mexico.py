# preprocessing/india_preprocessing.py
import pandas as pd

class MexicoPreprocessing:
    @staticmethod
    def load_and_preprocess(file_path):
        df = pd.read_excel(file_path)
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y %H:%M')

        df = df.drop(columns=['Data number'])
        for i in range(1, len(df) - 1):
            # Check if current row is '23:00' and the next is '00:00' of the next day
            if df['Date'].iloc[i].hour == 23 and df['Date'].iloc[i + 1].hour == 0 and df['Date'].iloc[i].day == df['Date'].iloc[i + 1].day:
                # print(df.at[i, 'Date'])
                # Adjust the '23:00' timestamp to the previous day
                df.at[i, 'Date'] = df['Date'].iloc[i] - pd.Timedelta(days=1)
        
        return df
