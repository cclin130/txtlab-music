# -*- coding: utf-8 -*-
"""
Created on Wed May  1 10:18:14 2019

@author: Cheng Lin
"""
import requests
import json
import base64

CLIENT_ID = 'd2450e9d8bdd43b69c3154c523a89ffb'
CLIENT_SECRET = '45cde74c8d5848a1bf4059d8e2bbeb2f'

GRANT_TYPE = 'client_credentials'
body_params = {'grant_type' : GRANT_TYPE}

url = 'https://api.spotify.com/v1/playlists/3jBAAylHWZAW48eFignBuh/tracks'


def get_access_token():
    r = requests.post('https://accounts.spotify.com/api/token',data=body_params, auth = (CLIENT_ID, CLIENT_SECRET))
    return r.json()['access_token']

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