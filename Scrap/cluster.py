import matplotlib.pyplot as plt, pandas as pd, numpy as np, matplotlib as mpl, requests, time
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from scipy.spatial.distance import cdist, pdist, euclidean
from sklearn.cluster import KMeans
from sklearn import metrics

pd.options.display.mpl_style = 'default' #load matplotlib for plotting
plt.style.use('ggplot') #im addicted to ggplot. so pretty.
mpl.rcParams['font.family'] = ['Bitstream Vera Sans']

df = pd.read_csv("final_data.csv")
print df
saveNames = df['Name']
df = df.drop(['Name'],1)
print df

# print df.columns

X = df.as_matrix()
X = scale(X)

print X

pca = PCA()
pca.fit(X)
var_expl = pca.explained_variance_ratio_
print var_expl
tot_var_expl = np.array([sum(var_expl[0:i+1]) for i,x in enumerate(var_expl)]) #create vector with cumulative variance
print tot_var_expl

# plt.figure(figsize=(12,4)) #create cumulative proportion of variance plot
# plt.subplot(1,2,1)
# plt.plot(range(1,len(tot_var_expl)+1), tot_var_expl*100,'o-')
# plt.axis([0, len(tot_var_expl)+1, 0, 100])
# plt.xlabel('Number of PCA Components Included')
# plt.ylabel('Percentage of variance explained (%)')

# plt.subplot(1,2,2) #create scree plot
# plt.plot(range(1,len(var_expl)+1), var_expl*100,'o-')
# plt.axis([0, len(var_expl)+1, 0, 100])
# plt.xlabel('PCA Component')
# plt.show(block=True)

reduced_data = PCA(n_components=6, whiten=True).fit_transform(X) #transform data into the 5 PCA components space
#kmeans assumes clusters have equal variance, and whitening helps keep this assumption.

k_range = range(2,31) #looking amount of variance explained by 1 through 30 cluster
k_means_var = [KMeans(n_clusters=k).fit(reduced_data) for k in k_range] #fit kmeans with 1 cluster to 30 clusters

#get labels and calculate silhouette score
labels = [i.labels_ for i in k_means_var]
sil_score = [metrics.silhouette_score(reduced_data,i,metric='euclidean') for i in labels]

centroids = [i.cluster_centers_ for i in k_means_var] #get the center of each cluster
k_euclid = [cdist(reduced_data,cent,'euclidean') for cent in centroids] #calculate distance between each item and each cluster center
dist = [np.min(ke,axis=1) for ke in k_euclid] #get the distance between each item and its cluster

wcss = [sum(d**2) for d in dist] #within cluster sum of squares
tss = sum(pdist(reduced_data)**2/reduced_data.shape[0]) #total sum of squares
bss = tss-wcss #between cluster sum of squares

# plt.clf()
# plt.figure(figsize=(12,4)) #create cumulative proportion of variance plot
# plt.subplot(1,2,1)
# plt.plot(k_range, bss/tss*100,'o-')
# plt.axis([0, np.max(k_range), 0, 100])
# plt.xlabel('Clusters')
# plt.ylabel('% of Var Explained')

# plt.subplot(1,2,2) #create scree plot
# plt.plot(k_range, np.transpose(sil_score)*100,'o-')
# plt.axis([0, np.max(k_range), 0, 40])
# plt.xlabel('Clusters')
# plt.ylabel('Avg Silhouette Score (Out of 100)')
# plt.show(block=True)

final_fit = KMeans(n_clusters=9).fit(reduced_data) #fit 6 clusters
df['kmeans_label'] = final_fit.labels_ #label each data point with its clusters
df['Name'] = saveNames #of course we want to know what players are in what cluster
# player_names = [pd.DataFrame(players_df[players_df['PERSON_ID']==x]['DISPLAY_LAST_COMMA_FIRST']).to_string(header=False,index=False) for x in df['PLAYER_ID']]
# # because playerID #s mean nothing to me, lets get the names too
# df['Name'] = player_names

#lets also create a dataframe with data about where the clusters occur in the 5 component PCA space.
cluster_locs = pd.DataFrame(final_fit.cluster_centers_,columns=['component %s'% str(s) for s in range(np.size(final_fit.cluster_centers_,1))])
#cluster_locs.columns = factor_names

print df
print cluster_locs

df.to_csv('stats_with_9clusters.csv')