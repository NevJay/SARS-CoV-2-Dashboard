import pandas as pd

df2 = pd.read_csv('new_data_set1.csv')
print(df2.duplicated().sum())

