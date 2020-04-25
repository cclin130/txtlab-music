# -*- coding: utf-8 -*-
"""
Created on Thur Apr 16

@author: Cheng Lin
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import date, timedelta
import pandas as pd

if __name__ == '__main__':
    # scrape from Jan 2003 to Dec 2008
    file_date = date(2005, 10, 29)
    end_date = date(2009, 1, 1)
    while file_date < end_date:
        print(file_date)
        billboard_100 = []
        page = requests.get(
            'https://www.billboard.com/charts/hot-100/' + str(file_date))

        # use bs4 on the rendered page to extract relevant info
        soup = BeautifulSoup(page.content, 'html.parser')

        chart_elems = soup.find_all(class_='chart-element__information')
        for entry in chart_elems:
            artist = entry.find(class_='chart-element__information__artist').get_text()
            track = entry.find(class_='chart-element__information__song').get_text()
            billboard_100.append([artist, track])

        # convert list to pandas dataframe, then save
        df_data = pd.DataFrame(billboard_100, columns=['artist', 'track'])
        # increment index so it matches billboard position number
        df_data.index = df_data.index + 1
        df_data.to_csv('billboard_data/'+str(file_date) +'.csv')

        # increment date by a week
        file_date = file_date + timedelta(days=7)
        time.sleep(120)

