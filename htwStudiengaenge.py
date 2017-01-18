import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get('http://www.htw-berlin.de/studium/studiengaenge/')

soup = BeautifulSoup(page.content, 'html.parser')

study_prog_table = soup.find('table', class_='key-value_table')

progs = study_prog_table.findAll('tr')

columns = [[] for x in range(8)]
headers = ['website', 'name', 'abschluss', 'form', 'typ', 'art', 'regelstudienzeit', 'ordnungen']
           
for prog in progs:
    cells = prog.findAll(['th', 'li'])
    
    columns[0].append(prog.find('th').find('a')['href'])
    columns[1].append(prog.find('th').get_text().strip())
    columns[2].append(prog.find(class_='togglable-switch').get_text().strip())
    columns[3].append(prog.find(text=re.compile('Form:')).split(":", 2)[1].strip())
    columns[4].append(prog.find(text=re.compile('Typ:')).split(":", 2)[1].strip())
    columns[5].append(prog.find(text=re.compile('Art:')).split(":", 2)[1].strip())
    columns[6].append(prog.find(text=re.compile('Regelstudienzeit:')).split(":", 2)[1].strip())

responses = []
page_links = ['/studium/ordnungen-module',
              '/studium/module-ordnungen',
              '/studium/ordnungen',
              '/studium/ordnungen-und-module/',
              '/studium/das-studium/ordnungen-module/',
              '/studium/das-studium/ordnungen-und-module/',
              '/studying/programme-regulations-module-descriptions/',
              '/studying/programme-regulations/']

for website in columns[0]:
    
    for page_link in page_links:
        prog_page = requests.get(website + page_link)
        if(prog_page.status_code == 200):
            break
        
    ordnungen = []
        
    if(prog_page.status_code == 200):
        soup = BeautifulSoup(prog_page.content, 'html.parser')
        downloads = soup.findAll('a', class_='download')
        for download in downloads:
            ordnungen.append([download.get_text(), download['href']])
    else:
        print('Invalid response code for: ' + website)
        
    responses.append([website, prog_page.status_code, downloads])
    columns[7].append(ordnungen)
    

df = pd.DataFrame(columns).transpose()
df.columns = headers
    
#df.iloc[[2]]
#df.loc[df['Name'].str.contains('Medieninformatik')]
#df.loc[df['Website'] == 'http://bau-bachelor.htw-berlin.de']


        

        

