# a python file with lots of helper functions for analysis
import pandas as pd
import numpy as np
import os, re
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