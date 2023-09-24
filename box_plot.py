import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the CSV files
df_transcript = pd.read_csv(r'C:\Users\USER\Desktop\test\5\transcript_times_33.csv', encoding='cp949')
df_fix = pd.read_csv(r'C:\Users\USER\Desktop\test\5\fix_33.csv')

# Create a new column for error count in each sentence
df_transcript['Error Count'] = 0

for i, row in df_fix.iterrows():
    mask = (df_transcript['Start_Time'] <= row['start_time']) & (df_transcript['End_Time'] >= row['end_time'])
    df_transcript.loc[mask, 'Error Count'] += 1

# Create a box plot of the error count
plt.figure(figsize=(10, 6))
plt.boxplot(df_transcript[df_transcript["Error Count"] > 0]['Error Count'].values, vert=False)  
plt.title('Box Plot of Error Word Counts')
plt.xlabel('Count')
plt.show()
