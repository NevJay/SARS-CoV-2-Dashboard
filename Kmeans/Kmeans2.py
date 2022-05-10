from sklearn.cluster import KMeans
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("new_data_set4.csv")
one_hot = pd.get_dummies(df['Sequence'])
print(one_hot.head(5))