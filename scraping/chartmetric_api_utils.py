# -*- coding: utf-8 -*-
"""
Created on Sun May  5 22:01:03 2019

@author: Cheng Lin
"""

import requests
import json
import time

# get chartmetric api token
def get_access_token(REFRESH_TOKEN):
    body_params = '{"refreshtoken" : "%s"}' % REFRESH_TOKEN
    
    r = requests.post('https://api.chartmetric.com/api/token',
                      data=body_params,
                      headers = {'Content-Type': 'application/json'})
    return r.json()['token']

# function to make generic api request
def make_api_request(url, token):
    status_code = 400
    while status_code != 200:
        response = requests.get(url, headers={'Authorization': 'Bearer {}'.format(token)})
        
        if status_code == 429:
            print('429 status code')
            time.sleep(80)
        
    return response.json()
