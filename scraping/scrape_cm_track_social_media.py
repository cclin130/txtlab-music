# -*- coding: utf-8 -*-
# script to pull chartmetric info on each unique track
# example usage:
# python scrape_cm_track_social_media.py \
#     '../spotify_data/all_unique_track_by_date.csv' 'REFRESH_TOKEN'

import sys
import csv
import time
import os

from chartmetric_api_utils import \
    get_access_token, make_api_request_nojson

if __name__ == '__main__':
    
    file_path = sys.argv[1]
    REFRESH_TOKEN = sys.argv[2]
    # ex usage: start point will be 2501 if unique_track_25.csv has already been returned
    start_point = sys.argv[3]
    
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
    head.extend(['youtube_views','shazam_count'])
    table = table[1:]

    # get access token
    print('---------get api access token------------')
    token = get_access_token(REFRESH_TOKEN)
    
    start_time = time.time()
    count = 0
    print('--------Scraping track metadata---------')
    for track in table:
        count += 1
        # skip tracks we've already returned
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
        # get date
        date = track[2]
        
        url = 'https://api.chartmetric.com/api/track/{0}/{1}/get-ids'\
            .format('spotify', track_id_spotify)

        response = make_api_request_nojson(url, token, REFRESH_TOKEN)
        
        if not response: continue

        response = response.json()
        if response['obj']:
            track_id_cm = response['obj'][0]['cm_track']
        else: continue

        platforms = ['youtube','shazam']
        
        for platform in platforms:
            # use chartmetric id to get track metadata
            url = 'https://api.chartmetric.io/api/track/{0}/{1}/stats?since={2}&until={2}'\
                .format(track_id_cm, platform, date)
            
            response = make_api_request_nojson(url, token, REFRESH_TOKEN)
            
            if not response: continue
            
            response = response.json()
            stat = response['obj']
            if stat:
                track.append(stat[0]['value'])
            else:
                track.append('')

        # writing to file every 1000th track
        if count % 1000 == 0:
            print('Writing file {}'.format(count%1000))
            f_p = '../spotify_data/track_social_data/unique_track_%s.csv' % \
                str((int) (count/1000))
            if not os.path.exists('../spotify_data/track_social_data'): 
                os.makedirs('../spotify_data/track_social_data')
            with open(f_p, encoding='utf-8', newline='', mode='w') as f:
                writer = csv.writer(f)
                writer.writerow(head)
                writer.writerows(table[0:count])
            f.close()
    
    # write data to file
    print('---------writing to file------------')
    with open(file_path, encoding='utf-8', newline='', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(head)
        writer.writerows(table)
    f.close()
