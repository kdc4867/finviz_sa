import os
from datetime import datetime
from src.data_loader import load_existing_data, save_data, load_stock_data
from src.sentiment_analysis import analyze_new_data
from src.scraper import scrape_finviz_news
from src.strategy_evaluation import evaluate_strategy
from src.analysis import load_and_prepare_data, analyze_correlation, simple_trading_strategy
import pandas as pd
from openai import OpenAI

def preprocess_data(df):
    # 'Date' 열을 datetime 객체로 변환
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df

def generate_summary(df, date):
    sentiment_counts = df['Sentiment'].value_counts()
    headlines = df['Headline'].tolist()
    
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    prompt = f"""Analysis Date: {date}

List of Headlines:
{', '.join(headlines)}

Sentiment Analysis Results:
Positive: {sentiment_counts.get('positive', 0)}
Neutral: {sentiment_counts.get('neutral', 0)}
Negative: {sentiment_counts.get('negative', 0)}

Based on the news headlines and sentiment analysis results above, please provide a detailed summary report in Korean following these instructions:

1. 뉴스 헤드라인 분석
   - Provide the exact counts of positive, neutral, and negative headlines.

2. 주요 뉴스 요약
   - Identify the main themes or categories that are most prominent in today's news.
   - For each identified theme:
     a) Provide a brief title for the theme.
     b) Include at least 2 relevant headlines verbatim, formatted as: **헤드라인**: *"Exact headline text"*
     c) Provide a brief analysis of these headlines and their implications in 2-3 sentences.

3. 결론
   - Summarize the overall market sentiment and key takeaways in 3-4 sentences.

Please write the entire summary in Korean, maintaining a professional tone suitable for financial analysis. Ensure that you directly quote relevant headlines in each section to support your analysis. The themes should reflect the most significant topics in today's news.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional financial news analyst providing comprehensive daily news summaries and insights for investors. Your task is to analyze English headlines and provide a detailed summary in Korean, with dynamically identified themes based on the day's most prominent news."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def save_summary(summary, date):
    summary_dir = 'data/summaries'
    os.makedirs(summary_dir, exist_ok=True)
    filename = f"{summary_dir}/summary_{date}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"Summary for {date} has been saved to {filename}")


if __name__ == "__main__":
    output_file = 'data/finviz_sentiment_analysis_results.csv'
    
    # 기존 데이터 로드
    existing_data = load_existing_data(output_file)
    
    # FinViz 뉴스 스크래핑
    print("FinViz 뉴스 스크래핑 중...")
    news_data = scrape_finviz_news()

    # 새로운 데이터 분석
    print("새로운 데이터 분석 중...")
    new_results = analyze_new_data(news_data, existing_data)
    
    if not new_results.empty:
        # 새 데이터와 기존 데이터 병합
        updated_results = pd.concat([new_results, existing_data])
        
        # 중복 제거 (Date와 Headline 기준으로)
        updated_results = updated_results.drop_duplicates(subset=['Date', 'Headline'], keep='first')
        
        # 날짜 기준으로 정렬
        updated_results = updated_results.sort_values('Date', ascending=False)
        
        # 결과 저장
        save_data(updated_results, output_file)
        
        # 최신 날짜의 데이터만 선택하여 요약 생성
        latest_date = updated_results['Date'].max()
        latest_data = updated_results[updated_results['Date'] == latest_date]
        
        print(f"Generating summary for {latest_date}")
        summary = generate_summary(latest_data, latest_date)
        save_summary(summary, latest_date)
        
        print(f"분석 결과가 {output_file} 파일로 저장되었습니다.")
        print(f"총 {len(updated_results)} 개의 항목이 저장되었습니다.")
    else:
        print("새로운 데이터가 없습니다.")
    # # 기존의 주가 데이터 분석 코드는 그대로 유지
    # print("\n주가 데이터 분석:")
    # companies = ['apple', 'amd', 'berkshire_hathaway', 'google', 'jpmorganchase',
    #              'meta', 'microsoft', 'nvidia', 'tesla', 'exxonmobil']
    # df = load_and_prepare_data(output_file, 'data/stock_prices.csv', companies)
    # analyze_correlation(df)
    # simple_trading_strategy(df)