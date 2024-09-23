# src/strategy_evaluation.py

import numpy as np
import pandas as pd

def evaluate_strategy(merged_df):
    # 롱-숏 전략
    merged_df['Position'] = np.where(merged_df['Sentiment_Score'] > 0, 1, np.where(merged_df['Sentiment_Score'] < 0, -1, 0))
    merged_df['Strategy_Return'] = merged_df['Position'] * merged_df['Return']

    # 누적 수익률 계산
    merged_df['Cumulative_Strategy_Return'] = (1 + merged_df['Strategy_Return']).cumprod()

    print(merged_df[['Date', 'Company', 'Cumulative_Strategy_Return']])
