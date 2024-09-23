# import pandas as pd
# from datetime import datetime

# def update_existing_data(input_file, output_file):
#     # CSV 파일 읽기
#     df = pd.read_csv(input_file)
    
#     # 현재 날짜 가져오기
#     current_date = datetime.now().date()
    
#     # 날짜 변환 함수
#     def convert_date(date_str):
#         if pd.isna(date_str):
#             return None
        
#         if ':' in date_str:  # 시간 형식 (예: "07:30AM")
#             return current_date
#         elif 'Jul' in date_str or 'Aug' in date_str:  # 날짜 형식 (예: "Jul-30")
#             try:
#                 date = datetime.strptime(f"{date_str}-{current_date.year}", "%b-%d-%Y").date()
#                 if date > current_date:
#                     date = date.replace(year=date.year - 1)
#                 return date
#             except ValueError:
#                 return None
#         else:
#             return None

#     # 'Date' 열 변환
#     df['Date'] = df['Date'].apply(convert_date)
    
#     # 날짜를 인덱스로 설정
#     df.set_index('Date', inplace=True)
    
#     # 날짜순으로 정렬
#     df.sort_index(inplace=True)
    
#     # 결과 저장
#     df.to_csv(output_file)
#     print(f"Updated data saved to {output_file}")

# # 함수 실행
# input_file = 'C:\\sa_project\\stock_data\\finviz_sentiment_analysis_results.csv'
# output_file = 'C:\\sa_project\\stock_data\\finviz_sentiment_analysis_results_updated.csv'
# update_existing_data(input_file, output_file)