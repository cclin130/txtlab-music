'''
script to normalize data
'''
import pandas as pd
from sklearn import preprocessing
import sys

if __name__ == '__main__':

    # getting input arguments
    if len(sys.argv) != 2:
        print('Input arguments are incorrect. Please include playlist type.')
        sys.exit()

    playlist_type = sys.argv[1]

    filepath = '../scraping/spotify_data/playlist_tracks/{}/{}_unique_auditory.csv'.format(playlist_type, playlist_type)

    print('---------- Reading CSV ----------')
    df = pd.read_csv(filepath)

    track_ids = df[['track_id']]
    x = df[['danceability','energy','key','loudness','mode','speechiness','instrumentalness','acousticness','valence','tempo']].values.astype(float)

    # Create a minimum and maximum processor object
    min_max_scaler = preprocessing.MinMaxScaler()

    # Create an object to transform the data 
    x_scaled = min_max_scaler.fit_transform(x)

    print('---------- Normalizing ----------')
    # Run the normalizer on the dataframe
    df_normalized = pd.DataFrame(x_scaled)
    # Adding column names
    df_normalized.columns = ['danceability','energy','key','loudness','mode','speechiness','instrumentalness','acousticness','valence','tempo']
    # Setting track_ids as indexes
    df_normalized['track_id'] = track_ids
    df_final = df_normalized.set_index('track_id')
    # Writting to file
    df_final.to_csv('../scraping/spotify_data/playlist_tracks/{}/{}_auditory_normalized.csv'.format(playlist_type, playlist_type))
