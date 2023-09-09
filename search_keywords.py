"""
사용자가 입력한 키워드가 포함된 문장들과 그 문장들의 시작 시간 및 종료 시간 정보를 csv 파일에서 찾아 변환함. 
"""
import csv

def search_keywords(keyword):
    results = []
    with open('D:/nlp_stt/aws_sentence_csv/transcript_times.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            sentence, start_time, end_time = row
            if keyword.lower() in sentence.lower(): 
                results.append((sentence, start_time, end_time))
    return results
