from joblib import load
import pandas as pd

# 모델 및 인코더 불러오기
model = load('rf_trained_model_company.joblib')
encoder = load('company_encoder.joblib')

# 사용자 입력 받기
print("Please enter the following values:")

# 입력 받을 컬럼명 리스트
columns = ['open', 'high', 'low', 'volume', 'Sentiment_Score', 'change_percent', 'ma5', 'rsi', 'company']

# 사용자로부터 입력 받기
input_data = []
for col in columns[:-1]:  # company 컬럼 제외
    value = float(input(f"Enter value for {col}: "))
    input_data.append(value)

company_name = input("Enter the company name: ")
company_encoded = encoder.transform([[company_name]]).toarray()[0]
input_data.extend(company_encoded)

# 입력 받은 데이터로 데이터프레임 생성
input_df = pd.DataFrame([input_data], columns=columns[:-1] + list(encoder.get_feature_names_out(['company'])))

# 예측 수행
prediction = model.predict(input_df)

# 예측 결과 출력
prediction_text = "up" if prediction[0] == 1 else "down"
print(f"The predicted price direction is: {prediction_text}")