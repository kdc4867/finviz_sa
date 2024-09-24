from openai import OpenAI
import json
import time
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def predict_sentiment(headline):
    try:
        prompt = f"Analyze the sentiment of the following headline and respond with only 'positive', 'negative', or 'neutral'. Headline: {headline}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a financial sentiment analyzer. Respond only with 'positive', 'negative', or 'neutral'."},
                {"role": "user", "content": prompt}
            ]
        )
        
        sentiment = response.choices[0].message.content.strip().lower()
        if sentiment not in ['positive', 'negative', 'neutral']:
            print(f"Unexpected sentiment: {sentiment}")
            return None
        return sentiment
    except Exception as e:
        print(f"API 호출 중 오류 발생: {str(e)}")
        return None

def analyze_new_data(news_df, existing_df):
    existing_headlines = set(existing_df['Headline'])
    new_results = []
    for date, row in news_df.iterrows():
        if row['Headline'] not in existing_headlines:
            sentiment = predict_sentiment(row['Headline'])
            if sentiment:
                new_results.append({
                    'Date': date,
                    'Headline': row['Headline'],
                    'Sentiment': sentiment
                })
            time.sleep(1)  # API 호출 제한을 피하기 위한 지연
    
    if new_results:
        return pd.DataFrame(new_results)
    else:
        return pd.DataFrame(columns=['Date', 'Headline', 'Sentiment'])