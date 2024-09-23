import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import pandas as pd
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv
# OpenAI 클라이언트 초기화
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def scrape_finviz_news():
    url = "https://finviz.com/news.ashx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_section = soup.find('div', id='news')
    current_date = datetime.now().date()
    news_data = []
    
    for row in news_section.find_all('tr', class_='styled-row'):
        date_cell = row.find('td', class_='news_date-cell')
        headline_cell = row.find('a', class_='nn-tab-link')
        if date_cell and headline_cell:
            time_str = date_cell.get_text(strip=True)
            headline = headline_cell.get_text(strip=True)
            
            # 날짜 처리
            if ':' in time_str:  # 시간 형식 (예: "07:30AM")
                news_date = current_date
            else:  # 날짜 형식 (예: "Jul-30")
                news_date = datetime.strptime(f"{time_str}-{current_date.year}", "%b-%d-%Y").date()
                if news_date > current_date:
                    news_date = news_date.replace(year=news_date.year - 1)
            
            news_data.append({'Date': news_date, 'Headline': headline})
    
    # 데이터프레임 생성 및 날짜를 인덱스로 설정
    df = pd.DataFrame(news_data)
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    
    return df

def predict_sentiment(headline):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Forget all your previous instructions. Pretend you are a financial expert. You are a financial expert with stock recommendation experience. Classify the sentiment of the following headline as neutral, positive, or negative. Reply only with JSON."},
                {"role": "user", "content": headline}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)['sentiment']
    except Exception as e:
        print(f"API 호출 중 오류 발생: {str(e)}")
        return None

def load_existing_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, index_col='Date', parse_dates=True)
    return pd.DataFrame(columns=['Headline', 'Predicted Sentiment'])

def analyze_new_data(news_df, existing_df):
    existing_headlines = set(existing_df['Headline'])
    new_results = []
    for date, row in news_df.iterrows():
        if row['Headline'] not in existing_headlines:
            sentiment = predict_sentiment(row['Headline'])
            new_results.append({
                'Date': date,
                'Headline': row['Headline'],
                'Predicted Sentiment': sentiment
            })
            time.sleep(1)  # API 호출 제한을 피하기 위한 지연
    
    new_df = pd.DataFrame(new_results).set_index('Date')
    return pd.concat([existing_df, new_df])

if __name__ == "__main__":
    output_file = r'C:\sa_project\data\finviz_sentiment_analysis_results_updated.csv'
    
    # 기존 데이터 로드
    existing_data = load_existing_data(output_file)
    
    # FinViz 뉴스 스크래핑
    print("FinViz 뉴스 스크래핑 중...")
    news_data = scrape_finviz_news()

    # 새로운 데이터 분석 및 기존 데이터와 병합
    print("새로운 데이터 분석 중...")
    updated_results = analyze_new_data(news_data, existing_data)

    # 결과 저장
    updated_results.to_csv(output_file)
    
    print(f"분석 결과가 {output_file} 파일로 저장되었습니다.")
    print(f"총 {len(updated_results)} 개의 항목이 저장되었습니다.")