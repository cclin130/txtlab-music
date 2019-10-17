# -*- coding: utf-8 -*-
# script to pull chartmetric info on each unique artist
# example usage:
# python scrape_cm_artist_data.py '../spotify_data/spotify_curated_unique_artist.csv' 'REFRESH_TOKEN'

import sys
import csv
import time

from chartmetric_api_utils import get_access_token, make_api_request

if __name__ == '__main__':
    
    file_path = sys.argv[1]
    REFRESH_TOKEN = sys.argv[2]
    
    # read csv
    print('---------reading csv------------')
    table = []
    with open(file_path, encoding = 'utf-8',mode='r+') as f:
        for line in f:
            # stop at first blank line
            if not line.split(',')[0]: break
            table.append(line.strip('\n').split(','))
    f.close()
    
    # modify table head to include new date
    head = table[0]
    head.extend(['gender', 'record_label', 'artist_country',
                 'current_city', 'hometown_city', 'band_members',
                 'spotify_description', 'spotify_tags'])
    table = table[1:]

    # get access token
    print('---------get api access token------------')
    token = get_access_token(REFRESH_TOKEN)
    
    start_time = time.time()
    print('--------Scraping artist metadata---------')
    for artist in table:
        # check if we need a new refresh token (every 25 min)
        if start_time - time.time() > 60*25:
            # get access token
            print('---------get api access token------------')
            token = get_access_token(REFRESH_TOKEN)
            start_time = time.time()

        print(artist[0])
        # first retrieve chartmetric artist id
        artist_id_spotify = artist[1]
        
        url = 'https://api.chartmetric.com/api/artist/{0}/{1}/get-ids'\
            .format('spotify', artist_id_spotify)
        
        response = make_api_request(url, token)
        artist_id_cm = response['obj'][0]['cm_artist']
        
        # use chartmetric id to get artist metadata
        url = 'https://api.chartmetric.io/api/artist/{}'\
            .format(artist_id_cm)
        
        response = make_api_request(url, token)
        
        artist_metadata = response['obj']
        
        # collect list of tags
        tags = []
        for tag in artist_metadata['tags']:
            tags.append(tag['name'])
        tags = '/'.join(tags) # separate tags with a slash
        
        artist.extend([
                artist_metadata['gender'],
                artist_metadata['record_label'],
                artist_metadata['code2'],
                artist_metadata['current_city'],
                artist_metadata['hometown_city'],
                artist_metadata['band_members'],
                artist_metadata['description'],
                tags
                ])
    
    # write data to file
    print('---------writing to file------------')
    with open(file_path, encoding='utf-8', newline='', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(head)
        writer.writerows(table)
    f.close()