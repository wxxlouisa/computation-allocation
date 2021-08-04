import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./source.post.csv')
df1 = df.groupby('column_1').mean()#.sort_values(by='score')
df2 = df.groupby('column_1').count()[['column_2']].rename(columns={'column_2':'cnt'})

sub_df = pd.concat([df1, df2], axis='columns').sort_values(by='score')
cnt_sum = sum(sub_df['cnt'])
score_sum = sum(sub_df['score'] * sub_df['cnt'])
sub_df['cusum'] = sub_df['cnt'].cumsum()
sub_df['score_cusum'] = (sub_df['score'] * sub_df['cnt']).cumsum()
sub_df['quantile'] = sub_df['cusum'] / cnt_sum
sub_df['score_quantile'] = sub_df['score_cusum'] / score_sum

plt.figure(figsize=(20, 10))
plt.plot(sub_df['quantile'].values, sub_df['score_quantile'].values)
plt.xlabel('drop ratio')
plt.ylabel('score loss ratio')
