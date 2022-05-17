import pandas as pd

df1 = pd.read_csv("D:/Data Science group project/final.csv")
print(df1["Location"].unique())
df1 = df1.replace(to_replace =["Braz", "Brazi", "Bra"], value ="Brazil")
df1 = df1.replace(to_replace =["Ita", "Ital"], value ="Italy")
df1 = df1.replace(to_replace =["Colo", "Colombi"],value ="Colombia")
df1 = df1.replace(to_replace =["I", "Indi"],value ="India")
df1 = df1.replace(to_replace =["P", "Polan","Pola"],value ="Poland")
df1 = df1.replace(to_replace =["Bangl"],value ="Bangladesh")


print(df1["Location"].unique())
df1.to_csv("D:/Data Science group project/final1.csv",index=False, sep=',')


