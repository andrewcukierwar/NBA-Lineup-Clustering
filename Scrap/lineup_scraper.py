# !python2
# coding: utf8
from bs4 import BeautifulSoup
import requests
import re
import sys
import numpy as np
import pandas as pd

lineup_list = []
url_base = "http://www.basketball-reference.com/play-index/plus/lineup_finder.cgi?request=1&match=single&player_id=&lineup_type=5-man&output=total&year_id=2017&is_playoffs=N&team_id=&opp_id=&game_num_min=0&game_num_max=99&game_month=&game_location=&game_result=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&order_by=pts&order_by_asc=&offset="
start_number = 0

while start_number <= 12300: # last page starts at 12300
	full_url = url_base + str(start_number)
	request = requests.get(full_url)
	html = request.text
	soup = BeautifulSoup(html, 'html.parser')
	content = soup.find('tbody').find_all('tr', class_='')
	for tag in content:
		lineup = {}
		all_tds = tag.find_all('td')
		for td in all_tds:
			if td["data-stat"] == "lineup":
				players = td.find_all('a')
				i = 1
				for a in players:
					if i == 1:
						lineup["Player1"] = str(a["data-tip"])
					elif i == 2:
						lineup["Player2"] = str(a["data-tip"])
					elif i == 3:
						lineup["Player3"] = str(a["data-tip"])
					elif i == 4:
						lineup["Player4"] = str(a["data-tip"])
					elif i == 5:
						lineup["Player5"] = str(a["data-tip"])
					i = i + 1
			if td["data-stat"] == "team_id":
				a = td.find('a')
				lineup["Team"] = str(a.text)
			if td["data-stat"] == "g":
				lineup["GP"] = int(td.text)
			if td["data-stat"] == "mp":
				lineup["MP"] = float(td.text)
			if td["data-stat"] == "poss":
				lineup["POSS"] = int(td.text)
			if td["data-stat"] == "opp_poss":
				lineup["DPOSS"] = int(td.text)
			if td["data-stat"] == "fg":
				lineup["FGM"] = int(td.text)
			if td["data-stat"] == "fga":
				lineup["FGA"] = int(td.text)
			if td["data-stat"] == "fg3":
				lineup["3PM"] = int(td.text)
			if td["data-stat"] == "fg3a":
				lineup["3PA"] = int(td.text)
			if td["data-stat"] == "ft":
				lineup["FTM"] = int(td.text)
			if td["data-stat"] == "fta":
				lineup["FTA"] = int(td.text)
			if td["data-stat"] == "pts":
				lineup["PTS"] = int(td.text)
		lineup_list.append(lineup)
	start_number = start_number + 100

df_offensive = pd.DataFrame(lineup_list, columns = ['Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Team', 'GP', 'MP', 'POSS', 'DPOSS', 'FGM', 'FGA', '3PM', '3PA', 'FTM', 'FTA', 'PTS'])
df_offensive.to_csv('lineups_offensive.csv')

lineup_list = []
url_base = "http://www.basketball-reference.com/play-index/plus/lineup_finder.cgi?request=1&match=single&player_id=&lineup_type=5-man&output=total&year_id=2017&is_playoffs=N&team_id=&opp_id=&game_num_min=0&game_num_max=99&game_month=&game_location=&game_result=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&order_by=opp_pts&order_by_asc=&offset="
start_number = 0

while start_number <= 12300: # last page starts at 12300
	full_url = url_base + str(start_number)
	request = requests.get(full_url)
	html = request.text
	soup = BeautifulSoup(html, 'html.parser')
	content = soup.find('tbody').find_all('tr', class_='')
	for tag in content:
		lineup = {}
		all_tds = tag.find_all('td')
		for td in all_tds:
			if td["data-stat"] == "lineup":
				players = td.find_all('a')
				i = 1
				for a in players:
					if i == 1:
						lineup["Player1"] = str(a["data-tip"])
					elif i == 2:
						lineup["Player2"] = str(a["data-tip"])
					elif i == 3:
						lineup["Player3"] = str(a["data-tip"])
					elif i == 4:
						lineup["Player4"] = str(a["data-tip"])
					elif i == 5:
						lineup["Player5"] = str(a["data-tip"])
					i = i + 1
			if td["data-stat"] == "team_id":
				a = td.find('a')
				lineup["Team"] = str(a.text)
			if td["data-stat"] == "g":
				lineup["GP"] = int(td.text)
			if td["data-stat"] == "mp":
				lineup["MP"] = float(td.text)
			if td["data-stat"] == "poss":
				lineup["POSS"] = int(td.text)
			if td["data-stat"] == "opp_poss":
				lineup["DPOSS"] = int(td.text)
			if td["data-stat"] == "opp_fg":
				lineup["DFGM"] = int(td.text)
			if td["data-stat"] == "opp_fga":
				lineup["DFGA"] = int(td.text)
			if td["data-stat"] == "opp_fg3":
				lineup["D3PM"] = int(td.text)
			if td["data-stat"] == "opp_fg3a":
				lineup["D3PA"] = int(td.text)
			if td["data-stat"] == "opp_ft":
				lineup["DFTM"] = int(td.text)
			if td["data-stat"] == "opp_fta":
				lineup["DFTA"] = int(td.text)
			if td["data-stat"] == "opp_pts":
				lineup["DPTS"] = int(td.text)
		lineup_list.append(lineup)
	start_number = start_number + 100

df_defensive = pd.DataFrame(lineup_list, columns = ['Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Team', 'GP', 'MP', 'POSS', 'DPOSS', 'DFGM', 'DFGA', 'D3PM', 'D3PA', 'DFTM', 'DFTA', 'DPTS'])
df_defensive.to_csv('lineups_defensive.csv')

df_total = df_offensive.merge(df_defensive, on=['Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Team', 'GP', 'MP', 'POSS', 'DPOSS'])
df_total.to_csv("lineups.csv", index=False)