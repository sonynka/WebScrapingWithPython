#https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/

import urllib
from bs4 import BeautifulSoup
import pandas as pd

wiki = 'https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India'

page = urllib.request.urlopen(wiki)

soup = BeautifulSoup(page, 'lxml')

links = soup.find_all('a')
tables = soup.find_all('table')
capitals_table = soup.find('table', class_='wikitable sortable plainrowheaders')

columns = [[] for x in range(7)]
headers = []
           
for row in capitals_table.findAll('tr'):
    cells = row.findAll(['td', 'th'])
    for idx, cell in enumerate(cells):
        columns[idx].append(cell.find(text=True))

for column in columns:
    headers.append(column.pop(0))
    
frame = pd.DataFrame(columns).transpose()
frame.columns = headers

        

        

