import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import matplotlib as plt
import re

# Get data from URL with requests.get
ua = UserAgent()

URL = 'https://www.nfl.com/stats/player-stats/'
page = requests.get(URL, headers={'User-Agent': ua.chrome})

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('table')
table_data = table.find_all('tr')

# Getting all the headings
headings = []
for th in table_data[0].find_all("th"):
    headings.append(th.text.replace('\n', ' ').strip())

# Getting the actual stats
table_stats = []
for tr in table.tbody.find_all("tr"):
    t_row = {}

    for td, th in zip(tr.find_all("td"), headings):
        t_row[th] = td.text.replace('\n', '').strip()
    table_stats.append(t_row)

# Converting to pandas df
stats_df = pd.DataFrame(table_stats)
print(stats_df)

# Convert all stats (but not Player Names) to numeric for data analysis
cols = stats_df.columns
stats_df[cols[1:]] = stats_df[cols[1:]].apply(pd.to_numeric, errors='coerce')

# Writing to CSV
stats_df.to_csv('NFL-Stats.csv')

# Example of visualization
stats_df.plot(x='Player', y='Pass Yds', kind='bar')

# Using RegEx (find stat categories with two-digit integers in them)
pattern = re.compile(r'[0-9]{2}')
matches = []
for i in range(0,len(headings)):
    matches.append(pattern.findall(headings[i]))
print(matches)