# from openai import OpenAI
# import pandas as pd
# import json

# # OpenAI 클라이언트 초기화
# client = OpenAI(api_key=your_openai_api_key)

# def prepare_data(file_path):
#     df = pd.read_csv(file_path)
#     return df[['Sentence', 'Sentiment']]

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
#         return json.loads(response.choices[0].message.content)
#     except Exception as e:
#         print(f"API 호출 중 오류 발생: {str(e)}")
#         return None

# if __name__ == "__main__":
#     # 데이터 준비
#     data = prepare_data(r'C:\sa_project\stock_data\old_data.csv')
#     print(f"로드된 데이터 샘플:\n{data.head()}\n")

#     # 새 헤드라인에 대한 예측
#     new_headlines = [
#         "Company XYZ reports record profits",
#         "Stock market plummets amid economic uncertainty",
#         "New technology breakthrough announced"
#     ]
    
#     for headline in new_headlines:
#         sentiment = predict_sentiment(headline)
#         if sentiment:
#             print(f"Headline: {headline}")
#             print(f"Predicted sentiment: {sentiment}")
#             print()
#         else:
#             print(f"'{headline}'에 대한 감성 예측 실패")