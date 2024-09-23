# import requests
# from bs4 import BeautifulSoup
# from openai import OpenAI
# import pandas as pd
# import json
# from sklearn.metrics import accuracy_score, classification_report
# import time
# import csv
# import os
# from datetime import datetime, timedelta
# # OpenAI 클라이언트 초기화
# client = OpenAI(api_key=your_openai_api_key)

# def scrape_finviz_news():
#     url = "https://finviz.com/news.ashx"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     news_section = soup.find('div', id='news')
#     current_date = datetime.now().date()
#     news_data = []
    
#     for row in news_section.find_all('tr', class_='styled-row'):
#         date_cell = row.find('td', class_='news_date-cell')
#         headline_cell = row.find('a', class_='nn-tab-link')
#         if date_cell and headline_cell:
#             time_str = date_cell.get_text(strip=True)
#             headline = headline_cell.get_text(strip=True)
            
#             # 날짜 처리
#             if ':' in time_str:  # 시간 형식 (예: "07:30AM")
#                 news_date = current_date
#             else:  # 날짜 형식 (예: "Jul-30")
#                 news_date = datetime.strptime(f"{time_str}-{current_date.year}", "%b-%d-%Y").date()
#                 if news_date > current_date:
#                     news_date = news_date.replace(year=news_date.year - 1)
            
#             formatted_date = news_date.strftime("%Y-%m-%d")
#             news_data.append({'date': formatted_date, 'headline': headline})
    
#     return news_data


# def predict_sentiment(headline):
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are a sentiment analysis assistant. Classify the sentiment of the following headline as neutral, positive, or negative. Reply only with JSON."},
#                 {"role": "user", "content": headline}
#             ],
#             response_format={"type": "json_object"}
#         )
#         return json.loads(response.choices[0].message.content)['sentiment']
#     except Exception as e:
#         print(f"API 호출 중 오류 발생: {str(e)}")
#         return None
# def load_existing_data(file_path):
#     if os.path.exists(file_path):
#         with open(file_path, 'r', newline='', encoding='utf-8') as file:
#             return list(csv.DictReader(file))
#     return []
# # def evaluate_model(data):
#     # true_labels = []
#     # predicted_labels = []
#     # for _, row in data.iterrows():
#     #     headline = row['Sentence']
#     #     true_sentiment = row['Sentiment']
#     #     predicted_sentiment = predict_sentiment(headline)
#     #     if predicted_sentiment:
#     #         true_labels.append(true_sentiment)
#     #         predicted_labels.append(predicted_sentiment)
#     #     time.sleep(1)  # API 호출 제한을 피하기 위한 지연
    
#     # accuracy = accuracy_score(true_labels, predicted_labels)
#     # report = classification_report(true_labels, predicted_labels)
#     # return accuracy, report

# def analyze_new_data(news_data, existing_data):
#     existing_headlines = set(item['Headline'] for item in existing_data)
#     results = existing_data
#     for news in news_data:
#         if news['headline'] not in existing_headlines:
#             sentiment = predict_sentiment(news['headline'])
#             results.append({
#                 'Date': news['date'],
#                 'Headline': news['headline'],
#                 'Predicted Sentiment': sentiment
#             })
#             time.sleep(1)  # API 호출 제한을 피하기 위한 지연
#     return results

# if __name__ == "__main__":
#     output_file = r'C:\sa_project\stock_data\finviz_sentiment_analysis_results.csv'
    
#     # 기존 데이터 로드
#     existing_data = load_existing_data(output_file)
    
#     # FinViz 뉴스 스크래핑
#     print("FinViz 뉴스 스크래핑 중...")
#     news_data = scrape_finviz_news()

#     # 새로운 데이터 분석 및 기존 데이터와 병합
#     print("새로운 데이터 분석 중...")
#     updated_results = analyze_new_data(news_data, existing_data)

#     # 결과 저장
#     with open(output_file, 'w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=['Date', 'Headline', 'Predicted Sentiment'])
#         writer.writeheader()
#         writer.writerows(updated_results)
    
#     print(f"분석 결과가 {output_file} 파일로 저장되었습니다.")
#     print(f"총 {len(updated_results)} 개의 항목이 저장되었습니다.")