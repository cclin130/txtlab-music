# -*- coding: utf-8 -*-
'''
Created on Wed Oct 16 2019

Script to calculate cosine similarity

@author: Benjamin LeBrun

-------------------------

Clarification for file naming:
2019-05-19-rem corresponds to the removals from 2019-05-12 playlist
2019-05-19-add corresponds to the additions to 2019-05-19 playlist

Here, for instance, we're comparing the additions to the may 19th playlist to the may 12th playlist and the removals from the may 12th
playlist to the tracks of the may 19th playlist.

'''
import pandas as pd
import numpy as np
import sys, os, re
from sklearn import preprocessing
from datetime import date, timedelta
from scipy import spatial

def normalize_min_max(tracks, track_ids):
    cols = ['danceability','energy','key','loudness','mode','speechiness',
            'instrumentalness','acousticness','valence','tempo']

    x = tracks[cols].values.astype(float)

    min_max_scaler = preprocessing.MinMaxScaler()

    x_scaled = min_max_scaler.fit_transform(x)

    df_normalized = pd.DataFrame(x_scaled)

    df_normalized.index = track_ids
    
    df_normalized.columns = cols
    
    return df_normalized

def normalize_mean(tracks, track_ids):
    cols = ['danceability','energy','key','loudness','mode','speechiness',
            'instrumentalness','acousticness','valence','tempo']
    normalized_df=(tracks[cols]-tracks[cols].mean())/(tracks[cols].std())
    
    normalized_df['track_id'] = track_ids
    df_final = normalized_df.set_index('track_id')

    return df_final

def cos_similarity(normalized_values, tracks, sub_ids):
    cos_sim = [];
    cols = ['danceability','energy','key','loudness','mode','speechiness','instrumentalness',
        'acousticness','valence','tempo']

    # Average track
    track_av = tracks[cols].mean()
    
    # Calculating similarity
    for row in sub_ids.iterrows():
        track = np.array(row[1])
        filt = normalized_values.index == track[0] # getting normalized track auditory values
        track_norm = normalized_values.loc[filt] # normalized track vales
        track_norm = track_norm[cols] # filtering correct column auditory values
        sim_value = 1 - spatial.distance.cosine(track_norm,track_av) # calculating cosine similarity
        cos_sim.append(sim_value) # appending to list
     
    return cos_sim

if __name__ == '__main__':

    # Getting input arguments
    if len(sys.argv) != 2:
        print('Input arguments are incorrect. Please include playlist type.')
        sys.exit()

    playlist_type = sys.argv[1]
    rootdir = '../spotify_data/playlist_tracks/%s/' % playlist_type

    for subdir, dirs, files in os.walk(rootdir):
        # Regex to avoid stepping into additions_and_removals dirs when walking through
        test_string = '.*\/additions_and_removals'
        test = re.fullmatch(test_string, format(subdir))

        if test: continue
        if subdir == rootdir: continue

        # Using date to call correct files
        file_date = date(2019, 5, 12)

        playlist_name = os.path.basename(str(subdir))

        print('---------- Calculating Similarity for %s ----------' % playlist_name)

        for x in range(len(files)-1):
            print('       Week %s       ' % str(x+1))
            
            # Additions compared to previous playlist (see file name clarification)
            add_date = file_date + timedelta(days=7)
            # Removals compared with current playlist (see file name clarification)
            rem_date = file_date 

            # Reading playlist and list IDs
            playlist = pd.read_csv(subdir + '/' + str(file_date) + '.csv')
            playlist_ids = playlist[['track_id']]
            
            # Additions
            if file_date == date(2019,8,25):
                pass # Edge case
            else:
                add_fp = subdir + '/additions_and_removals/' + str(add_date) + '-add.csv'
                add = pd.read_csv(add_fp)

                # Appending type to split after normalizing
                add['type'] = np.zeros(len(add), dtype=int)
                playlist['type'] = np.ones(len(playlist), dtype=int)

                # Merging to normalize
                add_ids = add[['track_id']]
                full = playlist.append(add, sort=False)
                full_ids = full[['track_id']]

                '''
                To Normalize Separately:

                playlist_ids = playlist[['track_id']]
                normalized_values = normalize_mean(playlist, playlist_ids)
                normalized_add = normalize_mean(add, add_ids)
                
                '''

                # Normalizing values   
                normalized_values = normalize_mean(full, full_ids)
                # Additions will be of type '1' 
                normalized_add = full[full['type']==1]

                cos_sim = cos_similarity(normalized_values, normalized_add, add_ids)
                add['cos_sim'] = cos_sim
                add.to_csv(add_fp, index=False)
               
            # Removals
            if file_date == date(2019,5,12):
                pass # Edge case
            else:
                rem_fp = subdir + '/additions_and_removals/' + str(rem_date) + '-rem.csv'
                rem = pd.read_csv(rem_fp)

                # Appending type to split after normalizing
                rem['type'] = np.zeros(len(rem), dtype=int)
                playlist['type'] = np.ones(len(playlist), dtype=int)
                    
                rem_ids = rem[['track_id']]
                full = playlist.append(rem, sort=False)
                full_ids = full[['track_id']]

                # Normalizing values
                normalized_values = normalize_mean(full, full_ids)
                # Removals will be of type '1'
                normalized_rem = full[full['type'] == 1]
                
                cos_sim = cos_similarity(normalized_values, normalized_rem, rem_ids)
                rem['cos_sim'] = cos_sim
                rem.to_csv(rem_fp, index=False)
                

            if file_date == date(2019, 8, 25):
                break
            else:
                file_date = file_date + timedelta(days=7)
