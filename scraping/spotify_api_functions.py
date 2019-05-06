# -*- coding: utf-8 -*-
"""
Created on Sun May  5 22:01:03 2019

@author: Cheng Lin
"""

import requests
import json
import base64
#from ratelimit import limits, sleep_and_retry

FIFTEEN_MINUTES = 900

def get_access_token(CLIENT_ID, CLIENT_SECRET):
    GRANT_TYPE = 'client_credentials'
    body_params = {'grant_type' : GRANT_TYPE}
    
    r = requests.post('https://accounts.spotify.com/api/token',data=body_params, auth = (CLIENT_ID, CLIENT_SECRET))
    return r.json()['access_token']

#function to make a generic spotify api call; returns a json
#@sleep_and_retry
#@limits(calls=30, period=60)
def make_api_request(url, token):
    r = requests.get(url, headers={'Authorization': 'Bearer {}'.format(token)})
    return r.json()

#function that pulls playlist contents given spotify playlist ID
def pull_playlist_contents(playlist_id):
    
    #request access token from spotify API
    token = get_access_token()
    #GET playlist tracks with API call using token
    url = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)
    r = requests.get(url, headers={'Authorization': 'Bearer {}'.format(token)})
    
    result = r.json()
    tracks = result['items']
    print('Retrieved {} tracks from playlist'.format(len(tracks)))

    return result