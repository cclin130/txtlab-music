# How to run scraping scripts

## Overview
For the purposes of this project, we will be scraping the following each week:

1. Number of followers for each playlist
2. Every [playlist track object](https://developer.spotify.com/documentation/web-api/reference/object-model/#track-object-full)
 present in the playlist, which includes:
  - track name
  - track id
  - date track was added to playlist
  - album name
  - release date
  - track duration (ms)
  - track poularity (spotify metric out of 100)
  - artist name
  - artist id
  - artist followers
  - artist poularity (spotify metric out of 100)
  - artist genres
3. Every playlist track object's [Spotify audio features](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/)
4. Each artist’s gender, race, age, sexual orientation*

*Note: #4 will be hand-annotated once all the artists have been collected

## Scraping scripts

This project requires two scripts, scrape_playlist_popularity.py and scrape_playlist_tracks_and_features.py
Both need to be run each week to collect the data.

### scrape_playlist_popularity.py

This script accepts a .csv file in the /scraping/spotify_data/playlist_popularity/ directory
containing playlist names and URI's and appends each playlist's
present follower count in an extra column. To call the script, first cd into the /scraping folder
and then run on your terminal:

```
python3 scrape_playlist_popularity.py <file_path_to_csv> <Spotify API Client ID> <Spotify API Client Secret>
```

For example,

```
python3 scrape_playlist_popularity.py playlist_popularity/spotify_curated_popularity.csv <CLIENT_ID> <CLIENT_SECRET>
```

### scrape_plyalist_tracks_and_features.py

This script accepts a .csv file containing playlist names and URI's, and scrapes all of the relevant
information for each track in each playlist. The script will then save one .csv file per playlist in
the /spotify_data/playlist_tracks/<playlist_type>/<folder name> directory. The .csv will be named the date.
The data collected for each track in each playlist will consist of all the features listed
in points 2 and 3 in the overview section.

To run the script, you must include the file path to the .csv with playlist names,
Spotify API Client ID, Spotify API Client Secret, and the playlist type (spotify_curated or user_curated)
Simply enter in your terminal:

```
python3 scrape_playlist_tracks_and_features.py <file_path_to_csv> <Spotify API Client ID>
<Spotify API Client Secret> <playlist type>
```

For example,

```
python3 scrape_playlist_tracks_and_features.py spotify_curated_playlists.csv <CLIENT_ID>
<CLIENT_SECRET> spotify_curated
```
