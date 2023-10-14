import pandas as pd
import matplotlib.pyplot as plt

df_transcript = pd.read_csv(r'C:\Users\USER\Desktop\test\5\transcript_times_33.csv', encoding='cp949')
df_fix = pd.read_csv(r'C:\Users\USER\Desktop\test\5\fix_33.csv')

df_transcript['Error Count'] = 0

for i, row in df_fix.iterrows():
    mask = (df_transcript['Start_Time'] <= row['start_time']) & (df_transcript['End_Time'] >= row['end_time'])
    df_transcript.loc[mask, 'Error Count'] += 1

error_counts = df_transcript['Error Count']
stats_info = error_counts.describe()

print("Median (Q2/50th percentile): ", stats_info['50%'])
print("First quartile (Q1/25th percentile): ", stats_info['25%'])
print("Third quartile (Q3/75th percentile): ", stats_info['75%'])
print("Minimum: ", stats_info['min'])
print("Maximum: ", stats_info['max'])

IQR = stats_info['75%'] - stats_info['25%']
outlier_threshold_upper = stats_info['75%'] + 1.5 * IQR
outlier_threshold_lower = max(0,stats_info["25%"] - 1.5 * IQR)

outliers_upper_range= error_counts[error_counts > outlier_threshold_upper]
outliers_lower_range= error_counts[error_counts < outlier_threshold_lower]

print("\nOutliers:")
for outlier in outliers_upper_range:
    print(outlier)

for outlier in outliers_lower_range:
    print(outlier)

plt.figure(figsize=(10, 6))
plt.boxplot(df_transcript[df_transcript["Error Count"] > 0]['Error Count'].values, vert=False)  
plt.title('Box Plot of Error Word Counts')
plt.xlabel('Count')
plt.show()