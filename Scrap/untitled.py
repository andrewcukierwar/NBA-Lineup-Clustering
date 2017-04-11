import matplotlib.pyplot as plt, pandas as pd, numpy as np, matplotlib as mpl, requests, time
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from scipy.spatial.distance import cdist, pdist, euclidean
from sklearn.cluster import KMeans
from sklearn import metrics

pd.options.display.mpl_style = 'default' #load matplotlib for plotting
plt.style.use('ggplot') #im addicted to ggplot. so pretty.
mpl.rcParams['font.family'] = ['Bitstream Vera Sans']

df = pd.read_json("players.json")
print df
# saveNames = df['Name']
# df = df.drop(['Name'],1)
# print df