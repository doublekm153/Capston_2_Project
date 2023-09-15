
import json
import csv
import string

def compare_and_correct_transcripts(reference_file, hypothesis_file, time_info_file):
    # 참조 텍스트와 가설 텍스트를 로드.
    with open(reference_file, 'r', encoding='utf8') as f:
        reference_text = f.read().split()

    with open(hypothesis_file, 'r', encoding='utf8') as f:
        hypothesis_json = json.load(f)

    # JSON 파일에서 전사 텍스트 추출.
    transcript_items = [item for item in hypothesis_json["results"]["items"] if item['type'] == "pronunciation"]

    # 참조와 가설 사이의 차이점을 찾음.
    differences = []
    
    for i in range(min(len(reference_text), len(transcript_items))):
       reference_word = reference_text[i].strip(string.punctuation)
       hypothesis_word = transcript_items[i]["alternatives"][0]["content"].strip(string.punctuation)
       
       if reference_word != hypothesis_word:
           differences.append({
               "reference_word": reference_word,
               "hypothesis_word": hypothesis_word,
               "start_time": float(transcript_items[i]['start_time']),
               "end_time": float(transcript_items[i]['end_time'])
           })

    # 시간 정보를 CSV 파일로 저장.
    with open(time_info_file, 'w', newline='', encoding='utf8') as csvfile:
       fieldnames = ['reference_word', 'hypothesis_word', 'start_time', 'end_time']
       writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
       
       writer.writeheader()
       
       for diff in differences:
           writer.writerow(diff)

# 사용
compare_and_correct_transcripts(
r"C:\Users\USER\Desktop\test\2\test_2.txt", 
r"C:\Users\USER\Desktop\test\2\test_2.json", 
r"C:\Users\USER\Desktop\\test\2\fix_2.csv"
)