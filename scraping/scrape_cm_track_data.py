# -*- coding: utf-8 -*-
# script to pull chartmetric info on each track
# example usage:
# python scrape_cm_track_data.py '../spotify_data/spotify_curated_unique_track.csv' 'REFRESH_TOKEN'

import sys
import csv
import time
import os

from chartmetric_api_utils import get_access_token, make_api_request

if __name__ == '__main__':
    
    file_path = sys.argv[1]
    REFRESH_TOKEN = sys.argv[2]
    # ex usage: start point will be 2501 if unique_artist_25.csv has already been returned
    start_point = sys.argv[3]
    
    # read csv
    print('---------reading csv------------')
    table = []
    with open(file_path, encoding = 'utf-8',mode='r+') as f:
        for line in f:
            # stop at first blank line
            if not line.split(',')[1]: break
            table.append(line.strip('\n').split(','))
    f.close()
    
    # modify table head to include new date
    head = table[0]
    head.extend(['album_label'])
    table = table[1:]

    # get access token
    print('---------get api access token------------')
    token = get_access_token(REFRESH_TOKEN)
    
    start_time = time.time()
    count = 0
    print('--------scraping track metadata---------')
    for track in table:
        count += 1
        # skip artists we've already returned
        if count < int(start_point): continue
    
        # check if we need a new refresh token (every 25 min)
        if time.time() - start_time > 60*25:
            # get access token
            print('---------get api access token------------')
            token = get_access_token(REFRESH_TOKEN)
            start_time = time.time()

        print(track[0])
        # first retrieve chartmetric track id
        track_id_spotify = track[1]
        
        url = 'https://api.chartmetric.io/api/track/{0}/{1}/get-ids'\
            .format('spotify', track_id_spotify)
        
        response = make_api_request(url, token)
        if response['obj']:
            track_id_cm = response['obj'][0]['cm_track']
        else: continue
        
        # use chartmetric id to get track metadata
        url = 'https://api.chartmetric.io/api/track/{}'\
            .format(track_id_cm)
        
        response = make_api_request(url, token)
        
        track_metadata = response['obj']
        if not track_metadata['albums']: continue
        
        track.extend([
                track_metadata['albums'][0]['label'],
                ])
    
        # write data to file every 1000th artist
        if count % 1000 == 0:
            f_p = '../spotify_data/track_data/unique_track_%s.csv' % \
                str((int) (count/1000))
            if not os.path.exists('../spotify_data/track_data'): 
                os.makedirs('../spotify_data/track_data')
            with open(f_p, encoding='utf-8', newline='', mode='w') as f:
                writer = csv.writer(f)
                writer.writerow(head)
                writer.writerows(table[0:count])
            f.close()
            
    print('---------writing to file------------')
    with open(file_path, encoding='utf-8', newline='', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(head)
        writer.writerows(table)
    f.close()