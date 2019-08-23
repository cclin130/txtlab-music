import pandas as pd
import numpy as np
import sys, os, re
from sklearn import preprocessing
from datetime import date, timedelta
from scipy import spatial

def cosine_similarity(tracks, track_ids, playlist_ids, normalized_data, filepath):
    sum1 = 0
    count = 0
    values = []
    cols = ['danceability','energy','key','loudness','mode','speechiness','instrumentalness','acousticness','valence','tempo']
    
    # looping through each track and comparing to whole playlist
    for row in track_ids.iterrows():
        track = np.array(row[1])
        filt = normalized_data['track_id'] == track[0] # getting normalized track auditory values from meta file
        track_norm = normalized_data.loc[filt] # normalized track vales
        track_norm = track_norm[cols] # filtering correct column auditory values
        count = 0
        sum1 = 0
            
        for row in playlist_ids.iterrows(): 
            track_comp = np.array(row[1])
            filt2 = normalized_data['track_id'] == track_comp[0] # setting filter using track_ids
            track_comp_norm = normalized_data.loc[filt2] # getting normalized track vales
            track_comp_norm = track_comp_norm[cols] # filetering correct column auditory values
            # skipping a track being compared to itself
            if track[0] == track_comp[0]:
                    continue
            sum1 = sum1 + 1 - spatial.distance.cosine(track_norm,track_comp_norm) # calculating cosine similarity
            count = count + 1

        # appending average similarity to track
        values.append(sum1/count)

    tracks['cos_sim'] = values
    
    #writting to file
    tracks.to_csv(filepath, index=False)

if __name__ == '__main__':

    # getting input arguments
    if len(sys.argv) != 2:
        print('Input arguments are incorrect. Please include playlist type.')
        sys.exit()

    playlist_type = sys.argv[1]
    rootdir = '../scraping/spotify_data/playlist_tracks/%s/' % playlist_type
    normalized_data = pd.read_csv('../scraping/spotify_data/playlist_tracks/%s/%s_auditory_normalized.csv' % (playlist_type, playlist_type))

    for subdir, dirs, files in os.walk(rootdir):
        # regex to avoid stepping into additions_and_removals dirs when walking through
        test_string = '.*\/additions_and_removals'
        test = re.fullmatch(test_string, format(subdir))

        if test: continue
        if subdir == rootdir: continue

        # using dates for files
        file_date = date(2019, 5, 19)

        playlist_name = os.path.basename(str(subdir))

        for x in range(len(files)-1):
            # reading files
            add_fp = subdir + '/additions_and_removals/' + str(file_date) + '-add.csv'
            add = pd.read_csv(add_fp)
            add_ids = add[['track_id']]
            rem_fp = subdir + '/additions_and_removals/' + str(file_date) + '-rem.csv'
            rem = pd.read_csv(rem_fp)
            rem_ids = rem[['track_id']]
            playlist = pd.read_csv(subdir + '/' + str(file_date) + '.csv')
            playlist_ids = playlist[['track_id']]

            # calculating and appending to meta file
            print("---------- calculating ", str(file_date), " of ", playlist_name, ' ----------')
            cosine_similarity(add, add_ids, playlist_ids, normalized_data, add_fp)
            cosine_similarity(rem, rem_ids, playlist_ids, normalized_data, rem_fp) 

            if file_date == date(2019, 8, 11):
                break
            else:
                file_date = file_date + timedelta(days=7)
    




    

    

    
