import pandas as pd
import numpy as np
from scipy import stats

def load_and_prepare_data(sentiment_file, stock_file, companies):
    # 감성 분석 결과 로드
    sentiment_df = pd.read_csv(sentiment_file)
    sentiment_df['Date'] = pd.to_datetime(sentiment_df['Date'], format='mixed').dt.date
    
    # 주가 데이터 로드
    stock_df = pd.read_csv(stock_file)
    stock_df['Date'] = pd.to_datetime(stock_df['Date']).dt.date
    
    # 기업 이름을 이용해 관련 뉴스 필터링
    sentiment_df['Relevant_Company'] = sentiment_df['Headline'].apply(
        lambda x: next((company for company in companies if company.lower() in x.lower()), None)
    )
    sentiment_df = sentiment_df.dropna(subset=['Relevant_Company'])
    
    # 감성을 수치화
    sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
    sentiment_df['Sentiment_Score'] = sentiment_df['Sentiment'].map(sentiment_map)
    
    # 날짜와 기업별로 감성 점수의 평균 계산
    daily_sentiment = sentiment_df.groupby(['Date', 'Relevant_Company'])['Sentiment_Score'].mean().reset_index()
    
    # 주가 데이터와 병합
    merged_df = pd.merge(stock_df, daily_sentiment, left_on=['Date', 'company'], right_on=['Date', 'Relevant_Company'], how='left')
    
    # 뉴스가 없는 날은 중립(0)으로 처리
    merged_df['Sentiment_Score'].fillna(0, inplace=True)
    
    # 5일 이동평균 감성 점수 계산
    merged_df['Sentiment_MA5'] = merged_df.groupby('company')['Sentiment_Score'].rolling(window=5).mean().reset_index(0, drop=True)
    
    return merged_df

def analyze_correlation(df):
    correlations = df.groupby('company').apply(lambda x: x['change_percent'].corr(x['Sentiment_Score']))
    print("각 기업별 감성 점수와 주가 변동의 상관계수:")
    print(correlations)
    
    # 전체 데이터에 대한 t-검정 수행
    t_stat, p_value = stats.ttest_ind(df['change_percent'].dropna(), df['Sentiment_Score'].dropna())
    print(f"\n전체 데이터 t-검정 결과 - t-통계량: {t_stat}, p-값: {p_value}")

def simple_trading_strategy(df):
    df['Position'] = np.where(df['Sentiment_MA5'] > 0, 1, 0)  # 감성 점수 5일 평균이 양수면 매수
    df['Strategy_Return'] = df['Position'].shift(1) * df['change_percent']
    
    results = df.groupby('company').agg({
        'Strategy_Return': ['sum', lambda x: x.mean() / x.std() * np.sqrt(252)]
    })
    results.columns = ['Total_Return', 'Sharpe_Ratio']
    
    print("\n각 기업별 트레이딩 전략 결과:")
    print(results)
    
    print(f"\n전체 포트폴리오 성과:")
    total_return = df['Strategy_Return'].sum()
    sharpe_ratio = df['Strategy_Return'].mean() / df['Strategy_Return'].std() * np.sqrt(252)
    print(f"총 수익률: {total_return:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

if __name__ == "__main__":
    sentiment_file = 'data/finviz_sentiment_analysis_results_updated.csv'
    stock_file = 'data/stock_prices.csv'
    companies = ['apple', 'amd', 'berkshire_hathaway', 'google', 'jpmorganchase',
                 'meta', 'microsoft', 'nvidia', 'tesla', 'exxonmobil']
    
    df = load_and_prepare_data(sentiment_file, stock_file, companies)
    
    print("상관관계 분석:")
    analyze_correlation(df)
    
    print("\n트레이딩 전략 시뮬레이션:")
    simple_trading_strategy(df)