# src/data_loader.py

import pandas as pd
import os
from datetime import datetime
def load_existing_data(file_path):
    try:
        # 먼저 Date 열을 문자열로 읽습니다
        df = pd.read_csv(file_path, dtype={'Date': str})
        
        # Date 열을 datetime으로 변환 시도
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # NaT 값을 제거하고 date 객체로 변환
        df = df.dropna(subset=['Date'])
        df['Date'] = df['Date'].dt.date
        
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Headline', 'Sentiment', 'Predicted Sentiment'])
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(columns=['Date', 'Headline', 'Sentiment', 'Predicted Sentiment'])

def save_data(df, file_path):
    # Date 열이 datetime 객체인 경우 문자열로 변환
    if pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    elif df['Date'].dtype == object:  # 이미 문자열인 경우
        pass
    else:  # date 객체인 경우
        df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d') if isinstance(x, datetime) else x)
    
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

def load_stock_data(file_path):
    return pd.read_csv(file_path, parse_dates=['Date'])
