# import time
# import pandas as pd
# from datetime import datetime, timedelta
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup

# def setup_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
    
#     service = Service('chromedriver')  # chromedriver 경로 설정
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     return driver

# def scrape_yahoo_finance_news(ticker, start_date, end_date):
#     driver = setup_driver()
#     base_url = f"https://finance.yahoo.com/quote/{ticker}/news"
    
#     driver.get(base_url)
    
#     news_data = []
#     last_height = driver.execute_script("return document.body.scrollHeight")
    
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)
        
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height
        
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         articles = soup.find_all('li', {'class': 'js-stream-content'})
        
#         for article in articles:
#             try:
#                 headline = article.find('h3').text.strip()
#                 date_str = article.find('time')['datetime']
#                 date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ').date()
                
#                 if start_date <= date <= end_date:
#                     news_data.append({
#                         'date': date.strftime('%Y-%m-%d'),
#                         'headline': headline
#                     })
#                     print(f"Scraped: {date.strftime('%Y-%m-%d')} - {headline}")
#             except Exception as e:
#                 print(f"Error processing article: {e}")
    
#     driver.quit()
#     return pd.DataFrame(news_data)

# # 사용 예시
# ticker = "AAPL"  # Apple Inc.의 티커 심볼
# start_date = datetime(2022, 1, 1).date()  # 시작 날짜
# end_date = datetime.now().date()  # 종료 날짜 (현재)

# news_df = scrape_yahoo_finance_news(ticker, start_date, end_date)

# print(news_df.head())
# print(f"Total news articles: {len(news_df)}")

# # CSV 파일로 저장
# news_df.to_csv(f'{ticker}_yahoo_finance_news_long.csv', index=False)
