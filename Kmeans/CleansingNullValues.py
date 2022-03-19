import pandas as pd

df1 = pd.read_csv('new_data_set.csv')
print(df1.isna().sum())
df1 = df1.dropna()
df1.to_csv('new_data_set1.csv', index=False)


