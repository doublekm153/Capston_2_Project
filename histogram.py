"""
히스토그램으로 표현하는 코드. 
설정한 파일에서 각 문장마다 오류율이 얼마나 나오는지 확인 가능. 
가로축은 해당 문장의 시작 시간
세로축은 오류 단어의 수. 
즉, 그래프가 없으면 오류 단어가 없는 문장.
그래프가 있는 문장은, 오류가 나오는 문장. 
세로축이 길수록, 해당 문장 안에 오류가 많이 있다는 의미. 
"""

import pandas as pd
import matplotlib.pyplot as plt

df_fix = pd.read_csv('C:\\Users\\USER\\Desktop\\test\\5\\fix_33.csv')
df_transcript = pd.read_csv('C:\\Users\\USER\\Desktop\\test\\5\\transcript_times_33.csv', encoding='cp949')

df_fix['sentence'] = None
df_fix['sentence_start_time'] = None

for i, row in df_fix.iterrows():
    for j, sent_row in df_transcript.iterrows():
        if row['start_time'] >= sent_row['Start_Time'] and row['end_time'] <= sent_row['End_Time']:
            df_fix.at[i, 'sentence'] = sent_row['Sentence']
            df_fix.at[i, 'sentence_start_time'] = sent_row['Start_Time']
            break

error_counts_per_sentence_start_time = df_fix['sentence_start_time'].value_counts()

plt.figure(figsize=(15,8))  
ax = error_counts_per_sentence_start_time.sort_index().plot(kind='bar')
plt.title('Frequency of Errors per Sentence Start Time')
plt.xlabel('Sentence Start Time')
plt.ylabel('Error Count')

for tick in ax.get_xticklabels():
    tick.set_rotation(45) 

plt.show()
