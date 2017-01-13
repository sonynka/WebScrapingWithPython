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

""" TUTORIAL WAY

A = []
B = []
C = []
D = []
E = []
F = []
G = []


for row in capitals_table.findAll('tr'):
    cells = row.findAll(['td', 'th'])
    
    if len(cells)==7 :
        A.append(cells[0].find(text=True))
        B.append(cells[1].find(text=True))
        C.append(cells[2].find(text=True))
        D.append(cells[3].find(text=True))
        E.append(cells[4].find(text=True))
        F.append(cells[5].find(text=True))
        G.append(cells[6].find(text=True))

df = pd.DataFrame()
df['Number'] = A
df['State/UT'] = B
df['Admin_Capital'] = C
df['Legislative_Capital'] = D
df['Judiciary_Capital'] = E
df['Year_Capital'] = F
df['Former_Capital'] = G

"""

columns = [[] for x in range(7)]
           
for row in capitals_table.findAll('tr'):
    cells = row.findAll(['td', 'th'])

    for idx, cell in enumerate(cells):
        columns[idx].append(cell.find(text=True))
        
headers = []

for column in columns:
    headers.append(column.pop(0))
    
frame = pd.DataFrame(columns).transpose()
frame.columns = headers

        

        

