# -*- coding: utf-8 -*-


import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd

years = list(range(1993,2023))

mvp_tables = []

for year in years:
    starting_url = "https://www.basketball-reference.com/awards/awards_{}.html"
    url = starting_url.format(year)
    data = requests.get(url)
    
    with open("mvp/{}.html".format(year), "w+", encoding="utf-8") as f:
        f.write(data.text)
     
    time.sleep(1)
    
for year in years:
    with open("mvp/{}.html".format(year), encoding="utf-8") as f:
        page = f.read()
        
    soup = BeautifulSoup(page, "lxml")
    soup.find("tr", class_="over_header").decompose()
    
    mvp_table = soup.find(id="mvp")
    mvp_df = pd.read_html(str(mvp_table))[0]
    mvp_df["Year"] = year
    mvp_tables.append(mvp_df)
  
mvp_table_all = pd.concat(mvp_tables)

mvp_table_all.to_csv("nba.csv")
mvp_table_all.to_excel("~/scrapping/nba.xlsx")

path = Service("~/Downloads/chromedriver_win32")
driver = webdriver.Chrome(service=path)

for year in years:
    starting_url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
    driver.get(starting_url.format(year))
    driver.execute_script("window.scrollTo(1,10000)")
    time.sleep(2)
    player_html = driver.page_source
    
    with open("player/{}.html".format(year), "w+", encoding="utf-8") as f:
        f.write(player_html)
        
player_per_game = []

for year in years:
    with open("player/{}.html".format(year), encoding="utf-8") as f:
        page = f.read()
        
    soup = BeautifulSoup(page, "lxml")
    remove_headers = soup.find_all("tr", class_="thead")
    
    for header in remove_headers:
        header.decompose()
        
    per_game_table = soup.find(id="per_game_stats")
    
    per_game_df = pd.read_html(str(per_game_table))[0]
    per_game_df["Year"] = year 
    
    player_per_game.append(per_game_df)
    
player_per_game_all = pd.concat(player_per_game)
player_per_game_all.to_excel("~/scrapping/player2.xlsx")

for year in years:
    starting_url = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html"
    url = starting_url.format(year)
    
    data = requests.get(url)
    
    with open("standings/{}.html".format(year), "w+", encoding="utf-8") as f:
        f.write(data.text)

standings = []

for year in years:
    with open("standings/{}.html".format(year), encoding="utf-8") as f:
        page = f.read()
        
    soup = BeautifulSoup(page, "lxml")
    remove_headers = soup.find_all("tr", class_="thead")
    
    for header in remove_headers:
        header.decompose()
        
    division = soup.find(id="divs_standings_E")
    division_df = pd.read_html(str(division))[0]
    division_df["Year"] = year
    division_df["Conference"] = division_df["Eastern Conference"]
    del division_df["Eastern Conference"]
    standings.append(division_df)
    
    division = soup.find(id="divs_standings_W")
    division_df = pd.read_html(str(division))[0]
    division_df["Year"] = year
    division_df["Conference"] = division_df["Western Conference"]
    del division_df["Western Conference"]
    standings.append(division_df)

standings_all = pd.concat(standings)
    
standings_all.to_excel("~/scrapping/standings.xlsx")