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
