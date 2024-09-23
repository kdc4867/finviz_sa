import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

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
    
    df = pd.DataFrame(news_data)
    df.set_index('Date', inplace=True)
    df.sort_index(ascending=False, inplace=True)
    
    return df