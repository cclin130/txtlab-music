# -*- coding: utf-8 -*-
"""
Created on Tue May  7 22:59:05 2019

@author: Cheng Lin
#script to scrape playlist contents and their features, then append it all to a new csv
"""
import csv
from datetime import date
from spotify_api_utils import get_access_token, make_api_request, pull_playlist_contents

if __name__ == '__main__':
    
    if len(sys.argv) != 5:
        print('Input arguments are incorrect.')
        print('Make sure to include csv file path, client ID, client secret, and spotify_curated/user_curated')
        sys.exit()
    
    #retrieve input arguments
    file_path = sys.argv[1]
    CLIENT_ID = sys.argv[2]
    CLIENT_SECRET = sys.argv[3]
    mode_input = sys.argv[4]
    
    if mode_input == 'spotify_data/playlist_tracks/spotify_curated':
        output_path = 'spotify_data/playlist_tracks/spotify_curated'
    else:
        output_path = 'user_curated'
        
    date = date.today()
    
    #read csv with playlist IDs
    print('---------reading playlist csv------------')
    table = []
    with open(file_path, encoding = 'utf-8',mode='r+') as f:
        for line in f:
            table.append(line.strip('\n').split(','))
    f.close()
    
    #loop through every playlist in the csv
    for line in table:
        token = get_access_token(CLIENT_ID, CLIENT_SECRET)
        playlist_id = line[1]
        
        result = pull_playlist_contents(playlist_id)
        
        #compile list of all tracks in the playlist
        #then pull all of their features
            