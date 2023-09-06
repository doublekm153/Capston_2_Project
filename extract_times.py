import json
import csv
import os
import glob

def extract_times():

    json_files = glob.glob("D:/nlp_stt/aws_json/*.json")

    latest_file = max(json_files, key=os.path.getctime)

    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data['results']['items']

    sentences = []
    sentence = ""
    start_time = None
    end_time = None

    for item in items:
        if 'start_time' in item and start_time is None:
            start_time = float(item['start_time'])

        sentence += " " + item['alternatives'][0]['content']

        if 'end_time' in item:
            end_time = float(item["end_time"])  

        if item['alternatives'][0]['content'] in ['.', '?', '!']:
            sentences.append((sentence.strip(), start_time, end_time))

            sentence = ""
            start_time = None
    
    csv_path='D:/nlp_stt/aws_sentence_csv'
    os.makedirs(csv_path, exist_ok=True)  
   
    with open(os.path.join(csv_path,'transcript_times.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Sentence", "Start_Time", "End_Time"])  

        for sent, stime, etime in sentences:
            writer.writerow([sent, stime, etime])  