# !python2
# coding: utf8
from bs4 import BeautifulSoup
import requests
import re
import sys
import numpy as np
import pandas as pd

player = {}
playerErr = []
try:
	link = "http://www.basketball-reference.com/players/c/curryst01/shooting/2017"
	sub_request = requests.get(link)
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
					player["Rim FGM"] = int(td.text)
				if td["data-stat"] == "fga":
					player["Rim FGA"] = int(td.text)
			tr_310 = sub_content[i+1]
			if tr_310 not in headers:
				print "Not in"
				tds_310 = tr_310.find_all('td')
				for td in tds_310:
					if td["data-stat"] == "fg":
						player["3-10 FGM"] = int(td.text)
					if td["data-stat"] == "fga":
						player["3-10 FGA"] = int(td.text)
			tr_1016 = sub_content[i+2]
			if tr_1016 not in headers:
				print "Not in"
				tds_1016 = tr_1016.find_all('td')
				for td in tds_1016:
					if td["data-stat"] == "fg":
						player["10-16 FGM"] = int(td.text)
					if td["data-stat"] == "fga":
						player["10-16 FGA"] = int(td.text)
			tr_1623 = sub_content[i+3]
			if tr_1623 not in headers:
				print "Not in"
				tds_1623 = tr_1623.find_all('td')
				for td in tds_1623:
					if td["data-stat"] == "fg":
						player["16-23 FGM"] = int(td.text)
					if td["data-stat"] == "fga":
						player["16-23 FGA"] = int(td.text)
except Exception, e:
	playerErr.append(link)
	print "Could not scrape all of player's stats"
print player

# sub_content = sub_soup.find('div', id="div_stats-nba-com").find_all('a')
# shooting_link = ""
# for a in sub_content:
# 	if a.text == "Shooting":
# 		shooting_link = a['href']
# 		shooting_request = requests.get(link)
# 		shooting_html = shooting_request.text
# 		shooting_soup = BeautifulSoup(shooting_html, 'html.parser')
# 		shooting_content = shooting_soup.find_all('div', class_='nba-stat-table')

# 		i = 1
# 		for tag in shooting_content:
# 			print i
# 			i = i + 1
# 		# 	if tag.text == "Restricted Area":
# 		# 		print "ye"
# 		print shooting_content
#print general_link


# div = sub_soup.find('div', {'id':"all_per_minute"})
# comments = sub_soup.findAll(text=lambda text:isinstance(text, BeautifulSoup.Comment))
# [comment.extract() for comment in comments]
# # print sub_soup.prettify()
# all_divs = div.find_all('div')
# for tag in all_divs:
# 	print tag['class']
# #print div
# table = div.find('table', {'id':"advanced"})
# print table

# # print subdiv
# tr = sub_soup.find('tr', {'id':'advanced.2017'})
# print tr
# # for tag in sub_content:
# all_tds = tr.find_all('td')
# for td in all_tds:
# 	if td["data-stat"] == "g":
# 		player["GP"] = int(td.text)


# # df = pd.DataFrame(lineup_list, columns = ['Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Team', 'GP', 'MP', 'POSS', 'DPOSS', 'FGM', 'FGA', '3PM', '3PA', 'FTM', 'FTA', 'PTS'])
# # df.to_csv('lineups_offensive.csv')
# print player