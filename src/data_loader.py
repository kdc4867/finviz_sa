# src/data_loader.py

import pandas as pd
import os

def load_existing_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, index_col='Date', parse_dates=True)
    return pd.DataFrame(columns=['Date', 'Headline', 'Company', 'Predicted Sentiment'])

def save_data(df, file_path):
    df.to_csv(file_path)

def load_stock_data(file_path):
    return pd.read_csv(file_path, parse_dates=['Date'])
