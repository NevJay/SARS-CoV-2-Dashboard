import pandas as pd
df2 = pd.read_csv("F:/DSGP/allnuc.csv", on_bad_lines='skip')
print(1)
df2 = df2.drop_duplicates(subset=["Sequence"], keep=False)
df2 = df2.dropna()
df2.to_csv("F:/DSGP/allnuc1.csv",index=False, sep=',')
print(2)
# list = df2['Sequence'].tolist()
# count = 0
# for j in range(len(list)):
#     for i in range(len(list[j])):
#         if list[j][i] == 'N':
#             df2.drop(df2.index[j], axis=0, inplace=True)
#             break
#
# print(len(df2))
# df2.to_csv("F:/DSGP/allnuc1.csv",index=False, sep=',')