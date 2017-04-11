# !python2
# coding: utf8
from bs4 import BeautifulSoup
import requests
import re
import sys
import numpy as np
import pandas as pd

players = []
playerErr = []
full_url = "http://www.basketball-reference.com/leagues/NBA_2017_advanced.html"
request = requests.get(full_url)
html = request.text
soup = BeautifulSoup(html, 'html.parser')
content = soup.find('tbody').find_all('tr', class_='full_table')
for tag in content:
	player = {}
	shooting_link = ""
	all_tds = tag.find_all('td')
	for td in all_tds:
		if td["data-stat"] == "player":
			a = td.find('a')
			player["Name"] = str(a.text)
			#a_href = "http://www.basketball-reference.com" + 
			a_href = a['href'].encode('utf-8')
			a_href = a_href[0:a_href.rfind('.')]
			shooting_link = "http://www.basketball-reference.com" + a_href + "/shooting/2017"
			#print shooting_link
		if td["data-stat"] == "g":
			player["GP"] = int(td.text)
		if td["data-stat"] == "mp":
			player["MP"] = int(td.text)
		if td["data-stat"] == "orb_pct":
			player["ORB%"] = float(td.text)
		if td["data-stat"] == "drb_pct":
			player["DRB%"] = float(td.text)
		if td["data-stat"] == "ast_pct":
			player["AST%"] = float(td.text)
		if td["data-stat"] == "usg_pct":
			player["USG%"] = float(td.text)
		if td["data-stat"] == "fta_per_fga_pct":
			if not td.text == "":
				player["FTR"] = float(td.text)
		if td["data-stat"] == "tov_pct":
			if not td.text == "":
				player["TOV%"] = float(td.text)
		if td["data-stat"] == "stl_pct":
			player["STL%"] = float(td.text)
	if player["MP"] < 100:
		print player["Name"] + " has played less than 100 minutes"
	else:
		try:
			sub_request = requests.get(shooting_link)
			sub_html = sub_request.text
			sub_soup = BeautifulSoup(sub_html, 'html.parser')
			sub_content = sub_soup.find('table', id='shooting').find_all('tr')
			headers = sub_soup.find('table', id='shooting').find_all('tr', class_='thead')
			for i in range(0,len(sub_content)):
					tr = sub_content[i]
					th = tr.find('th')
					if th.text == "Shot Distance":
						rim_tds = tr.find_all('td')
						for td in rim_tds:
							if td["data-stat"] == "fg":
								player["RIM FGM"] = int(td.text)
							if td["data-stat"] == "fga":
								player["RIM FGA"] = int(td.text)
						tr_310 = sub_content[i+1]
						if tr_310 not in headers:
							#print "Not in"
							tds_310 = tr_310.find_all('td')
							for td in tds_310:
								if td["data-stat"] == "fg":
									player["3-10 FGM"] = int(td.text)
								if td["data-stat"] == "fga":
									player["3-10 FGA"] = int(td.text)
						tr_1016 = sub_content[i+2]
						if tr_1016 not in headers:
							#print "Not in"
							tds_1016 = tr_1016.find_all('td')
							for td in tds_1016:
								if td["data-stat"] == "fg":
									player["10-16 FGM"] = int(td.text)
								if td["data-stat"] == "fga":
									player["10-16 FGA"] = int(td.text)
						tr_1623 = sub_content[i+3]
						if tr_1623 not in headers:
							#print "Not in"
							tds_1623 = tr_1623.find_all('td')
							for td in tds_1623:
								if td["data-stat"] == "fg":
									player["16-23 FGM"] = int(td.text)
								if td["data-stat"] == "fga":
									player["16-23 FGA"] = int(td.text)
		except Exception, e:
			playerErr.append(player)
			print "Could not scrape all stats of " + player["Name"]
		players.append(player)

total_url = "http://www.basketball-reference.com/leagues/NBA_2017_totals.html"
total_request = requests.get(total_url)
total_html = total_request.text
total_soup = BeautifulSoup(total_html, 'html.parser')
content = total_soup.find('tbody').find_all('tr', class_='full_table')
for tag in content:
	player = players[0]
	all_tds = tag.find_all('td')
	for td in all_tds:
		if td["data-stat"] == "player":
			a = td.find('a')
			player_name = str(a.text)
			#a_href = "http://www.basketball-reference.com" + 
			for p in players:
				if p["Name"] == player_name:
					player = p
		if td["data-stat"] == "fg3":
			player["3PM"] = int(td.text)
		if td["data-stat"] == "fg3a":
			player["3PA"] = int(td.text)
		if td["data-stat"] == "ft":
			player["FTM"] = int(td.text)
		if td["data-stat"] == "fta":
			player["FTA"] = int(td.text)
		if td["data-stat"] == "pf":
			player["PF"] = int(td.text)

df = pd.DataFrame(players, columns = ['Name', 'GP', 'MP', 'USG%', 'TOV%', 'STL%', 'AST%', 'ORB%', 'DRB%', 'FTR', 'PF', 'FTM', 'FTA', 'RIM FGM', 'RIM FGA', '3-10 FGM', '3-10 FGA', '10-16 FGM', '10-16 FGA', '16-23 FGM', '16-23 FGA', '3PM', '3PA'])
defensive_data = pd.read_csv("defensive_data.csv")
merged = df.merge(defensive_data, on='Name')
df.to_csv('player_stats.csv')
merged.to_csv('full_player_stats.csv')
print df
print len(players)