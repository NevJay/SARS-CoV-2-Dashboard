from sklearn.cluster import KMeans
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("output1.csv")
print(df.DNAENC)
scaler = MinMaxScaler()

df['DNAENC'] = scaler.fit_transform(df[['DNAENC']])

le = LabelEncoder()
df["Location"] = le.fit_transform(df["Location"])
df['Location'] = scaler.fit_transform(df[['Location']])
plt.scatter(df['Location'],df.DNAENC)
plt.xlabel('Location')
plt.ylabel('DNAENC')
#plt.show()

km = KMeans(n_clusters=3)
y_predicted = km.fit_predict(df[['Location','DNAENC']])
y_predicted
df['cluster']=y_predicted
km.cluster_centers_
score = silhouette_score(df[['Location','DNAENC']], km.labels_, metric='euclidean')
#
# Print the score
#
print('Silhouetter Score: %.3f' % score)
df1 = df[df.cluster==0]
df2 = df[df.cluster==1]
df3 = df[df.cluster==2]
plt.scatter(df1['Location'],df1['DNAENC'], color='green',label='cluster1')
plt.scatter(df2['Location'],df2['DNAENC'], color='red',label='cluster2')
plt.scatter(df3['Location'],df3['DNAENC'], color='yellow',label='cluster3')
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*',label='centroid')
plt.xlabel('Location')
plt.ylabel('DNAENC')
plt.legend()
plt.show()
scaler = MinMaxScaler()

# scaler.fit(df[['DNAENC']])
# df['DNAENC'] = scaler.transform(df[['DNAENC']])
#
# scaler.fit(df[['Location']])
# df['Location'] = scaler.transform(df[['Location']])
plt.scatter(df['Location'],df['DNAENC'])
plt.show()
sse = []
k_rng = range(1,10)
for k in k_rng:
    km = KMeans(n_clusters=k)
    km.fit(df[['Location','DNAENC']])
    sse.append(km.inertia_)

plt.xlabel('K')
plt.ylabel('Sum of squared error')
plt.plot(k_rng,sse)
plt.show()