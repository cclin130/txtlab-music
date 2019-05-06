import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
from time import sleep

if __name__ == '__main__':
    songs_file_path = 'Music_meta.csv'
    export_file_path = 'music_meta_features.csv'

    #instantiate spotify API wrapper
    cred_manager = SpotifyClientCredentials(client_id='d2450e9d8bdd43b69c3154c523a89ffb', client_secret='45cde74c8d5848a1bf4059d8e2bbeb2f')
    sp = spotipy.Spotify(client_credentials_manager=cred_manager)
    sp.trace=False

    #read in table of music data
    table = []
    file = songs_file_path
    with open(file, encoding='ISO-8859-1', mode='r+') as f:
        for line in f:
            line.encode('utf-8').strip()
            table.append(line.strip('\n').split(','))
    f.close()

    #store table's column headers eaprately; extend headers to hold more columns
    title = table[0]

    title.append('uri')
    title.append('danceability')
    title.append('energy')
    title.append('key')
    title.append('loudness')
    title.append('mode')
    title.append('speechiness')
    title.append('acousticness')
    title.append('instrumentalness')
    title.append('liveness')
    title.append('valence')
    title.append('tempo')
    title.append('duration_ms')
    title.append('time_signature')

    table = table[1:]

    #we want to loop through the csv of songs, finding the track's ID and then searching for its features
    for line in table:
        track_artist = line[1]
        track_title = line[2]
        print(track_title)

        sleep()
        results = sp.search(q=track_title, limit=1,type ='track')
        items = results['tracks']['items']

        if len(items) > 0:
            uri = items[0]['uri']
            track_features = sp.audio_features(uri)

            if track_features[0] is not None:
                for feature in title[6:]:
                    line.append(track_features[0][feature])

    #write to csv
    with open(export_file_path, encoding='utf-8', newline='', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(title)
        writer.writerows(table)
    f.close()