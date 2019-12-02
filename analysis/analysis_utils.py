# a python file with lots of helper functions for analysis
import pandas as pd
import numpy as np
import os
import re
from datetime import date, timedelta

# function to count amount playlist appearances of a label or group of labels' songs
# returns a dictionary with different values
def get_num_appearances(entries, column, curation):
    rootdir = '../spotify_data/playlist_tracks/%s/' % curation
    results = dict()
    
    for subdir, dirs, files in os.walk(rootdir):
        # Regex to avoid stepping into additions_and_removals dirs when walking through
        test_string = '.*\/additions_and_removals'
        test = re.fullmatch(test_string, format(subdir))

        if test: continue
        if subdir == rootdir: continue

        file_date = date(2019, 5, 12)

        playlist_name = os.path.basename(str(subdir))

        for x in range(len(files)-1):            
            playlist = pd.read_csv(subdir + '/' + str(file_date) + '.csv')
            
            # count # of playlist appearances
            playlist_count = len(pd.merge(entries[[column]], playlist[[column]], how='inner'))
            results['playlist_appearances'] = results.get('playlist_appearances', 0) + playlist_count
            
            # total number of playlist entries
            results['total_entries'] = results.get('total_entries', 0) + len(playlist)
            
            if file_date == date(2019, 8, 25):
                break
            else:
                file_date = file_date + timedelta(days=7)
           
    return results

# function that returns a list of indexes of tracks of a particular genre
def get_genre_list(data, genre_name):
    index=[]
    for i in range(0,len(data)):
        try:
            genres = data.iloc[i,12].split(',')
        except:
            continue
        for genre in genres:
            if re.match('.*'+genre_name+'.*', genre): 
                index.append(i)
                break

    return index

# function that returns a df with track count for each genre
def get_genres(playlist_type):
    df = pd.DataFrame()
    genre_list = []
    full_list = []
    unique_list = []
    counts = []
    rootdir = '../spotify_data/playlist_tracks/%s/' % playlist_type               
    for subdir, dirs, files in os.walk(rootdir):
            # Regex to avoid stepping into additions_and_removals dirs when walking through
            test_string = '.*\/additions_and_removals'
            test = re.fullmatch(test_string, format(subdir))
            
            if test: continue
            if subdir == rootdir: continue

            file_date = date(2019, 5, 12)

            playlist_name = os.path.basename(str(subdir))
            track_count = 0
            total_count = 0
            for x in range(len(files)-1):
                playlist = pd.read_csv(subdir + '/' + str(file_date) + '.csv')
                for i in range(0, len(playlist)):                     
                    genres = playlist.iloc[i,11]
                    if genres is np.nan: 
                        continue
                    else:
                        genre_list = genres.split(',')
                
                    full_list = full_list + genre_list
                
                if file_date == date(2019, 8, 25): break
                else:
                    file_date = file_date + timedelta(days=7)

    for genre in full_list:
        if genre not in unique_list:
            unique_list.append(genre)
            count = full_list.count(genre)
            counts.append(count)
    
    df['genre'] = unique_list
    df['count'] = counts
    return df


def get_label_count(label_list):
    label_dict = {}

    for i in range(0,len(label_list)):
        labels = label_list.iloc[i,0]
        if labels is np.nan: continue
        labels = labels.split('/')
        for label in labels:
            label_dict[label] = label_dict.get(label, 0) + 1

    labels = pd.DataFrame.from_dict(label_dict, orient = 'index').reset_index()
    labels.columns = ['label', 'count']
    return labels

# function to return a df of all tracks 
def get_all_tracks():
    df = pd.DataFrame()
    
    for subdir, dirs, files in os.walk(rootdir):
        # Regex to avoid stepping into additions_and_removals dirs when walking through
        test_string = '.*\/additions_and_removals'
        test = re.fullmatch(test_string, format(subdir))

        if test: continue
        if subdir == rootdir: continue

        file_date = date(2019, 5, 12)

        playlist_name = os.path.basename(str(subdir))

        for x in range(len(files)-1):            
            playlist = pd.read_csv(subdir + '/' + str(file_date) + '.csv')
            
            df = pd.concat([df,playlist])
            
            
            if file_date == date(2019, 8, 25):
                break
            else:
                file_date = file_date + timedelta(days=7)
           
    return results

# function to obtain intersection of genres
# returns a (symmetrical) dataframe with counts
def get_genre_intersections(df):
    genre_dict = {'hh': 'hip-hop','hs': 'house','rk': 'rock',
                  'bl': 'blues','ct': 'country','el': 'electronic',
                  'fk': 'folk','jz': 'jazz','la': 'latin',
                  'pp': 'pop','rb': 'r&b/soul','in': 'indie','rp': 'rap'}
    count = 0
    dset = pd.DataFrame()
    for genre1 in genre_dict:
        intersection_list = []
        for genre2 in genre_dict:
            #if genre1 == genre2: continue
            genre1_tracks = df[df['genre'] == genre1]
            genre2_tracks = df[df['genre'] == genre2]
            intersection = len(pd.merge(genre1_tracks[['index']], genre2_tracks[['index']], how='inner'))
            intersection_list.append(intersection)
        dset[genre1] = intersection_list
    
    cols = ['hip-hop','house','rock','blues','country','edm','folk','jazz','latin','pop','r&b','indie','rap']
    dset.index = cols
    dset.index = cols
    
    return dset

def get_label_and_gender(df):
    artist_data = pd.read_csv('../spotify_data/all_unique_artist.csv')
    track_data = pd.read_csv('../spotify_data/all_unique_track.csv')

    meta_gender = []
    meta_label = []
    artist_id = df.iloc[3,9]
    track_id = df.iloc[2,2]
    for i in range(0,len(df)):
        artist_id = df.iloc[i,9]
        track_id = df.iloc[i,2]
        if i % 3000 == 0 and not i == 0:
            print('%s percent complete' % str(int(i/len(df)*100)))
        filt1 = artist_data['artist_id'] == artist_id
        filt2 = track_data['track_id'] == track_id
        try:
            gender = artist_data[filt1].iloc[0,2]
        except:
            gender = np.nan
        try:
            label = track_data[filt2].iloc[0,2]
        except:
            label = np.nan
            
        meta_gender.append(gender)
        meta_label.append(label)
        
    assert len(meta_gender) == len(df)
    assert len(meta_label) == len(df)
    df['gender'] = meta_gender
    df['label'] = meta_label
    
    return df

# function to obtain intersection of genres
# returns dataframe with proportions of a genres songs in another
def get_genre_intersection_props(df):
    genre_dict = {'hh': 'hip-hop','hs': 'house','rk': 'rock',
                  'bl': 'blues','ct': 'country','el': 'electronic',
                  'fk': 'folk','jz': 'jazz','la': 'latin',
                  'pp': 'pop','rb': 'r&b/soul','in': 'indie','rp': 'rap'}
    count = 0
    dset = pd.DataFrame()
    for genre1 in genre_dict:
        intersection_list = []
        for genre2 in genre_dict:
            #if genre1 == genre2: continue
            genre1_tracks = df[df['genre'] == genre1]
            genre2_tracks = df[df['genre'] == genre2]
            intersection = len(pd.merge(genre1_tracks[['index']], genre2_tracks[['index']], how='inner'))
            intersection_list.append(intersection/len(genre1_tracks))
        dset[genre1] = intersection_list
    
    dset.index = ['hip-hop','house','rock','blues','country','edm','folk','jazz','latin','pop','r&b','indie','rap']
    
    return dset

# function to get gender distribution for a df
# returns float64
def get_gender_distribution(df):
    male = len(df[df['gender'] == 1])
    female = len(df[df['gender'] == 0])
    nan = len(df[df['gender'].isna()])
    total = len(df) - nan

    return (male/total)

# function that returns a df with the 
def get_track_label_concentration(label, playlist_type):
    unique_tracks = pd.read_csv('../spotify_data/all_unique_track.csv')
    tracks = unique_tracks[unique_tracks['album_label'] == label]
    df = pd.DataFrame()
    list_names = []
    perc = []
    track_counts = []
    rootdir = '../spotify_data/playlist_tracks/%s/' % playlist_type               
    for subdir, dirs, files in os.walk(rootdir):
            # Regex to avoid stepping into additions_and_removals dirs when walking through
            test_string = '.*\/additions_and_removals'
            test = re.fullmatch(test_string, format(subdir))
            
            if test: continue
            if subdir == rootdir: continue

            file_date = date(2019, 5, 12)

            playlist_name = os.path.basename(str(subdir))
            track_count = 0
            total_count = 0
            for x in range(len(files)-1):
                playlist = pd.read_csv(subdir + '/' + str(file_date) + '.csv')
                track_count += len(pd.merge(tracks[['track_id']], playlist[['track_id']], how='inner'))
                total_count += len(playlist)
                
                if file_date == date(2019, 8, 25): break
                else:
                    file_date = file_date + timedelta(days=7)
            
            list_names.append(playlist_name)
            perc.append(track_count/total_count)
            track_counts.append(total_count)
            
    df['playlist'] = list_names
    df['total_track_count'] = track_counts
    df['%'] = perc
              
    return df.sort_values(by=['%'], ascending=False)

# function that returns playlist with more than 20% of its songs belonging to a certain label 
def independence_test(playlist_type):
    # looking at top 100 labels
    susp_labels = []
    for i in range(0,100):
        label = labels_sorted.iloc[i,0]
        df = get_track_label_concentration(label, playlist_type)    
        if df.iloc[0,2] >= 0.20:
            susp_labels.append(label)

    return susp_labels

#function that returns a df with weekly percentages of tracks from a playlist that belong to a given record label
def get_playlist_label_count(label, playlist_name):
    unique_tracks = pd.read_csv('../spotify_data/all_unique_track.csv')
    tracks = unique_tracks[unique_tracks['album_label'] == label]
    nan_tracks = unique_tracks[unique_tracks['album_label'].isna()]
    df = pd.DataFrame()
    weeks = []
    perc = []
    track_counts = []
    rootdir = '../spotify_data/playlist_tracks/user_curated/%s/' % playlist_name

    file_date = date(2019, 5, 12)

    while(file_date != date(2019, 9, 1)):
        track_count = 0
        total_count = 0
        nan_count = 0
        week = str(file_date)
        playlist = pd.read_csv(rootdir + str(week) + '.csv')
        track_count = len(pd.merge(tracks[['track_id']], playlist[['track_id']], how='inner'))
        total_count = len(playlist)
        nan_count = len(pd.merge(nan_tracks[['track_id']], playlist[['track_id']], how='inner'))
    
        weeks.append(week)
        perc.append(track_count/(total_count-nan_count))
        track_counts.append(total_count)
        
        file_date = file_date + timedelta(days=7)
            
    df['week'] = weeks
    df['total_track_count'] = track_counts
    df['%'] = perc
    
    return df.sort_values(by=['%'], ascending=False)

# function that returns a df of all entries in a playlist
# with only the index_cols of that playlist
def get_all_entries(curation, index_cols):
    rootdir = '../spotify_data/playlist_tracks/%s/' % curation
    
    dfs_all = []
    for playlist in os.listdir(rootdir):
        if not os.path.isdir(rootdir + '/' + playlist): continue
        
        for file in os.listdir(rootdir + '/' + playlist):           
            filepath = rootdir + '/' + playlist + '/' + file
            if os.path.isdir(filepath): continue

            dfs_all.append(pd.read_csv(filepath)[index_cols])

    return pd.concat(dfs_all)

def gini(array):
    """Calculate the Gini coefficient of a numpy array."""
    # based on bottom eq:
    # http://www.statsdirect.com/help/generatedimages/equations/equation154.svg
    # from:
    # http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    # Values must be sorted:
    array = np.sort(array)
    # Index per array element:
    index = np.arange(1,array.shape[0]+1)
    # Number of array elements:
    n = array.shape[0]
    # Gini coefficient:
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))
