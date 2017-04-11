#import libraries and tell ipython we want inline figures rather than interactive figures. 
import matplotlib.pyplot as plt, pandas as pd, numpy as np, matplotlib as mpl, requests, time

# %matplotlib inline
pd.options.display.mpl_style = 'default' #load matplotlib for plotting
plt.style.use('ggplot') #im addicted to ggplot. so pretty.
mpl.rcParams['font.family'] = ['Bitstream Vera Sans']

url = 'http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=2015-16'
# the critical part of the URL is IsOnlyCurrentSeason=0. The 0 means all seasons.
response = requests.get(url) #get data
headers = response.json()['resultSets'][0]
players = response.json()['resultSets'][0]['rowSet']
players_df = pd.DataFrame(players, columns=headers['headers']) #turn data into dataframe


players_df['TO_YEAR'] = players_df['TO_YEAR'].apply(lambda x:int(x)) #change data in the TO_YEAR column from strings to numbers
players_df = players_df[players_df['TO_YEAR']>1979] #only use players after 3 pt line

print players_df