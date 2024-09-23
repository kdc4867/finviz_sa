# main.py

import os
from src.data_loader import load_existing_data, save_data, load_stock_data
from src.sentiment_analysis import analyze_new_data
from src.scraper import scrape_finviz_news
from src.strategy_evaluation import evaluate_strategy
from src.analysis import load_and_prepare_data, analyze_correlation, simple_trading_strategy
import pandas as pd

if __name__ == "__main__":
    output_file = 'data/finviz_sentiment_analysis_results_updated.csv'
    
    # 기존 데이터 로드
    existing_data = load_existing_data(output_file)
    
    # FinViz 뉴스 스크래핑
    print("FinViz 뉴스 스크래핑 중...")
    news_data = scrape_finviz_news()

    # 새로운 데이터 분석 및 기존 데이터와 병합
    print("새로운 데이터 분석 중...")
    new_results = analyze_new_data(news_data, existing_data)
    if not new_results.empty:
        new_results.set_index('Date', inplace=True)
        updated_results = pd.concat([new_results, existing_data])
    else:
        updated_results = existing_data

    # 결과 저장
    save_data(updated_results, output_file)
    

    print(f"분석 결과가 {output_file} 파일로 저장되었습니다.")
    print(f"총 {len(updated_results)} 개의 항목이 저장되었습니다.")

    print("\n주가 데이터 분석:")
    companies = ['apple', 'amd', 'berkshire_hathaway', 'google', 'jpmorganchase',
                 'meta', 'microsoft', 'nvidia', 'tesla', 'exxonmobil']
    df = load_and_prepare_data(output_file, 'data/stock_prices.csv', companies)
    analyze_correlation(df)
    simple_trading_strategy(df)
