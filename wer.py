"""
성능평가 부분. 
WER(World Error Rate) 계산하는 코드. 
WER : 자동 음성 인식(ASR) 시스템의 출력 결과와 실제 참조 텍스트 간의 차이를 측정하는 데 사용되는 지표. 
Levenshtein 거리 알고리즘을 사용하여 두 텍스트 사이의 WER 계산. 
사람의 정확도 측정 : Ground Truth == 사람이 제공하는 정보를 기준으로 aws transcribe 의 성능 평가. 
즉, 어떤 단어나 문장이 올바르게 인식되었는지, 오류가 있다면 오류율은 얼마나 되는지 확인. 
word error rate(WER) 등의 지표 변화를 그래프로 나타낼 수 있음. 
Ground Truth : 참조 스크립트
시스템 출력(AWS transcribe) : 가설 스크립트
"""
import numpy as np
import matplotlib.pyplot as plt
import json

# Levenshtein 거리 알고리즘을 사용하여 두 텍스트 사이의 Word Error Rate 계산. 
# Levenshtein 거리 == 한 문자열을 다른 문자열로 변환하기 위해 필요한 최소한의 수정 연산 횟수. 
def calculate_wer(reference, hypothesis):
    # reference와 hypothesis를 단어 단위로 분할
    reference = reference.split()
    hypothesis = hypothesis.split()

    #Levenshtein distance matrix d를 초기화
    d = np.zeros((len(reference)+1)*(len(hypothesis)+1), dtype=np.uint8)
    d = d.reshape((len(reference)+1, len(hypothesis)+1))
    
    # Levenshtein 거리 행결 d 의 첫 번째 행과 열 초기화. 
    for i in range(len(reference)+1):
        for j in range(len(hypothesis)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # 실제 Levenshtein 거리 계산 수행. 
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

    # WER 점수 계산 -> 백분율 형태로 나타냄. 
    wer_score= float(d[len(reference)][len(hypothesis)]) / len(reference) * 100
    
    return wer_score

# AWS Transcribe 결과와 Ground Truth 읽기 
with open(r'C:\Users\USER\Desktop\test\1\test_1.json', 'r', encoding='utf8') as f:
     transcribe_result_text=json.load(f)["results"]["transcripts"][0]["transcript"]

with open(r'C:\Users\USER\Desktop\test\1\test_1.txt', 'r', encoding='utf8') as f:
     ground_truth_text=f.read()



wer_score=calculate_wer(transcribe_result_text , ground_truth_text )

# WER 결과 출력 
print(f'WER: {wer_score}%')

# WER 시각화 
plt.bar('WER', wer_score)
plt.ylim(0,100)
plt.ylabel('Error Rate (%)')
plt.title('Word Error Rate')
plt.show()
