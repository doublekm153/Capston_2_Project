"""
참조 스크립트, 가설 스크립트의 wer 를 막대그래프로 표현. 
"""

import numpy as np
import matplotlib.pyplot as plt
import json

def calculate_wer(reference, hypothesis):
    reference = reference.split()
    hypothesis = hypothesis.split()

    d = np.zeros((len(reference)+1)*(len(hypothesis)+1), dtype=np.uint8)
    d = d.reshape((len(reference)+1, len(hypothesis)+1))
    
    for i in range(len(reference)+1):
        for j in range(len(hypothesis)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    for i in range(1, len(reference)+1):
        for j in range(1, len(hypothesis)+1):
            if reference[i-1] == hypothesis[j-1]:
                cost = 0
            else:
                cost = 2
                
            substitution = d[i-1][j-1] + cost
            insertion    = d[i][j-1] + 2
            deletion     = d[i-1][j] + 2
            
            d[i][j] = min(substitution, insertion, deletion)

    wer_score= float(d[len(reference)][len(hypothesis)]) / len(reference) * 100
    
    return wer_score

files_list=['test_11','test_22', 'test_33'] 
wer_scores=[]
for file_name in files_list:
    
    with open(f'C:\\Users\\USER\\Desktop\\test\\5\\{file_name}.json', 'r', encoding='utf8') as f:
        aws_transcribe_result_text=json.load(f)["results"]["transcripts"][0]["transcript"]

    with open(f'C:\\Users\\USER\\Desktop\\test\\5\\{file_name}.txt', 'r', encoding='utf8') as f:
        ground_truth_text=f.read()

     
     # WER 점수 계산 후 wer_scores 리스트에 추가 
    wer_score=calculate_wer(aws_transcribe_result_text , ground_truth_text )
    wer_scores.append(wer_score)

# WER 시각화 
plt.bar(files_list , wer_scores)
plt.ylim(0,60)
plt.ylabel('Error Rate (%)')
plt.title('Word Error Rate')
plt.show()
