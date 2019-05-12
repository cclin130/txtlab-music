# -*- coding: utf-8 -*-
"""
Created on Tue May  7 22:59:05 2019

@author: Cheng Lin
#script to scrape playlist contents and their features, then append it all to a new csv
"""
import sys, os, csv
from datetime import date
import time
from spotify_api_utils import get_access_token, make_api_request#, pull_50_playlist_contents

if __name__ == '__main__':
    
    if len(sys.argv) != 5:
        print('Input arguments are incorrect.')
        print('Make sure to include csv file path, client ID, client secret, and spotify_curated/user_curated')
        sys.exit()
    
    #retrieve input arguments
    file_path = sys.argv[1]
    CLIENT_ID = sys.argv[2]
    CLIENT_SECRET = sys.argv[3]
    playlist_type = sys.argv[4]
    
    if playlist_type == 'spotify_curated':
        output_path = 'spotify_data/playlist_tracks/spotify_curated'
    else:
        output_path = 'spotify_data/playlist_tracks/user_curated'
        
    date = date.today()
    
    #read csv with playlist IDs
    print('---------reading playlist csv------------')
    table = []
    with open(file_path, encoding = 'utf-8',mode='r+') as f:
        for line in f:
            table.append(line.strip('\n').split(','))
    f.close()
    
    #get rid of headings in table
    table=table[1:]
    playlist_data_table_head = ['track_name','track_id','date_added',
                     'album_name','release_date', 'track_duration_ms', 'track_popularity',
                     'artist', 'artist_id','artist_followers',
                     'artist_popularity','artist_genres',
                     'danceability','energy','key','loudness','mode','speechiness','acousticness',
                     'instrumentalness','liveness','valence','tempo','time_signature']
    audio_feature_list = ['danceability','energy','key','loudness','mode','speechiness','acousticness',
                     'instrumentalness','liveness','valence','tempo','time_signature']

    
    #loop through every playlist in the csv
    print('---------scraping playlist contents and song features--------')
    for line in table:
        playlist_name = line[0].replace(' ', '_')
        token = get_access_token(CLIENT_ID, CLIENT_SECRET)
        playlist_id = line[1]
        
        print('----------{}----------'.format(playlist_name))
        #GET playlist tracks with API call using token
        url = 'https://api.spotify.com/v1/playlists/{}/tracks?limit=50'.format(playlist_id)
        
        playlist_data_table=[]
        acoustic_features_table=[]
        artist_data_table=[]
        while True:
            result = make_api_request(url, token)
            tracks = result['items']
            print('Retrieved {0} tracks from {1}'.format(len(tracks),playlist_name))
            
            print('collecting track data...')
            track_uris = []
            artist_uris = []
            for track in tracks:
                track_obj = track['track']
                
                #check if we've reached the end of the list
                if track_obj is None:
                    break
                
                #save track uri to pull features
                track_uris.append(track_obj['id'])
                #save main artist's uri to pull artist popularity
                artist_uris.append(track_obj['artists'][0]['id'])
                
                #add rest of the track data to a list to append to playlist_data_table
                track_data = [track_obj['name'],track_obj['id']]
                track_data.append(track['added_at'])
                track_data.append(track_obj['album']['name'])
                track_data.append(track_obj['album']['release_date'])
                track_data.append(track_obj['duration_ms'])
                track_data.append(track_obj['popularity'])
                
                #append track_data list to playlist_data_table
                playlist_data_table.append(track_data)
                
            #given the return tracks, pull all of their acoustic features
            #up to 50 tracks at once
            print('collecting acoustic features...')
            track_uris_str = ','.join(track_uris)
            url = ('https://api.spotify.com/v1/audio-features/'+
                    '?ids={}').format(track_uris_str)
            acoustic_features = make_api_request(url, token)['audio_features']
            for feature_list in acoustic_features:
                feature_data = []
                if feature_list is not None:
                    for feature in audio_feature_list:
                        feature_data.append(feature_list[feature])
                
                acoustic_features_table.append(feature_data)
            
            #next pull all of their artist data
            print('collecting artist data...')
            artist_uris_str = ','.join(artist_uris)
            url = 'https://api.spotify.com/v1/artists?ids={}'.format(artist_uris_str)
            artist_data = make_api_request(url, token)['artists']
            for artist in artist_data:
                artist_data = [artist['name'],artist['id']]
                artist_data.append(artist['followers']['total'])
                artist_data.append(artist['popularity'])
                artist_data.append(','.join(artist['genres']))
                
                artist_data_table.append(artist_data)
                
            #the api request returns a parameter to tell us if we retrieved the entire playlist or not
            #this is since the web API limits the num. of tracks pulled at once to 100
            if (result['next'] != None):
                url = result['next']
            else:
                break
        
        #with the three lists of data (playlist data, feature data, artist data),
        #compile all into one list
        for i in range(0, len(playlist_data_table)):
            playlist_data_table[i].extend(artist_data_table[i])
            playlist_data_table[i].extend(acoustic_features_table[i])
            
        #create a csv for the playlist on that day
        print('-----------saving {} data to csv----------'.format(playlist_name))
        output_file_folder = '{0}/{1}'.format(output_path, playlist_name)
        if not os.path.isdir(output_file_folder):
            os.mkdir(output_file_folder)
            
        with open(output_file_folder+'/'+str(date)+'.csv', encoding='utf-8', newline='', mode='w') as f:
            writer = csv.writer(f)
            writer.writerow(playlist_data_table_head)
            writer.writerows(playlist_data_table)
        f.close()