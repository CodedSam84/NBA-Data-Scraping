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

driver.get("https://www.basketball-reference.com/leagues/NBA_1993_per_game.html")
driver.execute_script("window.scrollTo(1,10000)")
time.sleep(2)
players_1993 = driver.page_source
print(players_1993)

with open("player/1993.html", "w+", encoding="utf-8") as f:
    f.write(players_1993)