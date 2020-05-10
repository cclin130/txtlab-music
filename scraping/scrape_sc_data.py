'''
06/05/2020
Script to scrape singles chronology, i.e. billboard record labels
Author: Benjamin LeBrun
'''

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def get_year(year):
    response = requests.get('https://singleschronology.com/%s-2/' % year)
    data = response.text
    soup = BeautifulSoup(data,'html.parser')
    
    tables = soup.find_all("table")
    # 12 months
    assert len(tables) == 12
    billboard = []
    
    for table in tables:
        rows = table.find_all('td')
        # table has 6 columns
        assert len(rows)%6 == 0
        cell_num = 0
        while cell_num < len(rows):
            billboard.append([re.sub('<[^<]+?>', '', str(rows[cell_num])), 
                              re.sub('<[^<]+?>', '', str(rows[cell_num+1])), 
                              re.sub('<[^<]+?>', '', str(rows[cell_num+2])), 
                              re.sub('<[^<]+?>', '', str(rows[cell_num+3])), 
                              re.sub('<[^<]+?>', '', str(rows[cell_num+5]))])
            cell_num += 6
            
    df = pd.DataFrame(billboard, columns=['release_date', 'peak', 'artist', 'track', 'label'])
    
    return df

if __name__ == '__main__':

    for year in [2001,2002,2003,2004,2005,2006,2007,2008]:
        tracks = get_year(year)
        tracks.to_csv('../billboard_data/sc/' + str(year) + '.csv', index=False)
