# -*- coding: utf-8 -*-
"""
Created on Sun May  5 21:49:15 2019

@author: Cheng Lin
"""
import sys
import csv
from datetime import date
from spotify_api_functions import get_access_token, make_api_request

if __name__ == '__main__':
    
    #retrieve input arguments
    file_path = sys.argv[1]
    CLIENT_ID = sys.argv[2]
    CLIENT_SECRET = sys.argv[3]
    
    #read csv
    print('---------reading csv------------')
    table = []
    with open(file_path, encoding = 'utf-8',mode='r+') as f:
        for line in f:
            table.append(line.strip('\n').split(','))
    f.close()
    
    #modify table head to include new date
    head = table[0]
    head.append('{}_followers'.format(date.today()))
    table = table[1:]
    
    #get access token
    print('---------get api access token------------')
    token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    
    #loop through table lines and query playlist popularity
    print('---------make api calls for # of playlist followers------------')
    for line in table:
        playlist_id = line[1]
        url = 'https://api.spotify.com/v1/playlists/{}?fields=followers'.format(playlist_id)
        
        result = make_api_request(url, token)

        num_followers = result['followers']['total']
        line.append(num_followers)
        print('{0} playlist has {1} followers'.format(line[0], num_followers))

    with open(file_path, encoding='utf-8', newline='', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(head)
        writer.writerows(table)
    f.close()