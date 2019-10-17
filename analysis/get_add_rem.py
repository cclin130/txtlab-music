'''
script to sort additions and removals

the script walks through each directory, concatenates lists being compared, removes duplicates, and filters additions and removals based on 'new' or 'old' keywords

'''

import pandas as pd
import os, sys, re
from datetime import date, timedelta

if __name__ == '__main__':

    if len(sys.argv) != 2:
        raise InputError('Must enter playlist_type as argument')

    #retrieve input argument
    playlist_type = sys.argv[1]

    rootdir = '../spotify_data/playlist_tracks/%s/' % playlist_type

    for subdir, dirs, files in os.walk(rootdir):
        #regex to avoid stepping into additions_and_removals dirs when walking through
        test_string = '.*\/additions_and_removals'
        test = re.fullmatch(test_string, format(subdir))
        if test:
            continue

        print('---{}---'.format(os.path.basename(str(subdir))))

        #setting dates to compare files
        start_date = date(2019, 5, 12)
        next_date = start_date + timedelta(days=7)

        #to avoid creation of an 'additions_and_removals' folder in rootdir while walking through
        if subdir == rootdir:
            continue
        
        if os.path.exists(subdir + '/additions_and_removals') == False:
            os.makedirs(subdir + '/additions_and_removals')
            
        
        for x in range(len(files)-1):
            #filenames
            file1 = subdir + '/' + str(start_date) + '.csv'
            file2 = subdir + '/' + str(next_date) + '.csv'

            if os.path.exists(file2) == False:
                print("filepath error at {}, for {} \n".format(subdir, file2))
                continue
    
            #files to be written to
            file3 = subdir + '/additions_and_removals/{}-add.csv'.format(next_date)
            file4 = subdir + '/additions_and_removals/{}-rem.csv'.format(next_date)

            old = pd.read_csv(file1, parse_dates=True)
            new = pd.read_csv(file2, parse_dates=True)

            #appending new column
            old['version'] = 'old'
            new['version'] = 'new'
    
            #concatenate playlists
            full_set = pd.concat([old, new], ignore_index=True)
        
            #getting two lists of duplicate tracks
            dupe_names_rem = full_set.set_index('track_id').index.duplicated(keep='last')
            dupe_names_add = full_set.set_index('track_id').index.duplicated(keep='first')

            #getting removals by filtering out duplicates
            dupe_rem = full_set[~dupe_names_rem]
            #removals will be ones with 'old' keyword
            removals = dupe_rem[(dupe_rem['version'] == 'old')]

            #getting additions by fitlering out duplicates
            dupe_add = full_set[~dupe_names_add]
            #additions will have 'new' keyword
            additions = dupe_add[(dupe_add['version'] == 'new')]

            #dropping 'version' column
            additions = additions.drop(['version'], axis=1)
            removals = removals.drop(['version'], axis=1)

            #reading to csv
            additions.to_csv(file3, index=False)
            removals.to_csv(file4, index=False)

            #resetting dates for file names
            start_date = next_date
            temp = start_date
            next_date = temp + timedelta(days=7)

