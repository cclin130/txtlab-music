# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 07:30:10 2019

Script to get all unique entries in all playlists

@author: Cheng Lin
"""

import os
import sys
import pdb
import pandas as pd

if __name__ == '__main__':
    playlist_type = sys.argv[1]
    index_column = sys.argv[2]
    
    if index_column == 'artist':
        index_cols = ['artist','artist_id']
    elif index_column == 'track':
        index_cols = ['track_name','track_id'] 
    elif index_column == 'auditory':
        index_cols = ['track_name', 'track_id', 'danceability', 'energy', 'key', 'loudness', 'mode','speechiness','instrumentalness', 'acousticness', 'valence', 'tempo']
    else:
        raise InputError('Invalid index column')
    
    if len(sys.argv) != 3:
        raise InputError('Must have playlist_type and index_col as arguments')
    
    rootdir = '../scraping/spotify_data/playlist_tracks/%s/' % playlist_type
    
    dfs_all = []
    for playlist in os.listdir(rootdir):
        dfs_playlist = []
        if not os.path.isdir(rootdir + '/' + playlist): continue
        
        print('-----------Getting unique %s entries for %s-----------' % 
              (index_column, playlist))
        for file in os.listdir(rootdir + '/' + playlist):           
            filepath = rootdir + '/' + playlist + '/' + file
            if os.path.isdir(filepath): continue

            dfs_playlist.append(pd.read_csv(filepath)[index_cols])
            
            # if first csv in folder, go to next iteration
            if len(dfs_playlist) == 1: continue
            # drop duplicates on spotify URI
            df_concat_playlist = \
                pd.concat(dfs_playlist).drop_duplicates(subset=[index_cols[1]])
            dfs_playlist = [df_concat_playlist]
        
        # check that dfs_temp finishes with one dataframe
        assert len(dfs_playlist) == 1, 'dfs_playlist does not have length 1'
        
        # add playlist results to final list 'dfs'
        dfs_all.append(dfs_playlist[0])
        
        # if first playlist
        if len(dfs_all) == 1: continue
        # drop suplicates on spotify URI
        df_concat_all = pd.concat(dfs_all).drop_duplicates(subset=[index_cols[1]])
        dfs_all = [df_concat_all]
        
    assert len(dfs_all) == 1, 'dfs_all does not have length 1'
    # save to csv
    dfs_all[0].to_csv(
            rootdir + playlist_type + '_unique_' + index_column + '.csv', index=False)
            
