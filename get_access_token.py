#!/bin/env python3
# -*- coding: UTF-8 -*-
'''
Created on 2016/09/22

@author: nkasai
'''
import sys
import argparse
from requests_oauthlib.oauth1_session import OAuth1Session

CONSUMER_KEY = 'enter your consumer key'
CONSUMER_SECRET = 'enter your consumer secret'

REQUEST_TOKEN_URL = 'https://api.zaim.net/v2/auth/request'
AUTHORIZE_URL = 'https://www.zaim.net/users/auth'
ACCESS_TOKEN_URL = 'https://api.zaim.net/v2/auth/access'
CALLBACK_URI = 'https://localhost/'  # dummy

def main(args):
    """
    main
    """
    ret = 0
    
    try:
        oauth = OAuth1Session(
            CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            callback_uri=CALLBACK_URI
        )
        
        fetch_response = oauth.fetch_request_token(REQUEST_TOKEN_URL)
        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        
        #print('resource_owner_key', resource_owner_key)
        #print('resource_owner_secret', resource_owner_secret)
        
        auth_url = oauth.authorization_url(AUTHORIZE_URL)
        
        print('enter this auth url into browser.', auth_url)
        print('and get the verifier(from html source).')
        print('')
        
        verifier = input('input verifier:')
        
        oauth = OAuth1Session(
            CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret
        )
        
        fetch_response = oauth.fetch_access_token(ACCESS_TOKEN_URL, verifier=verifier)
        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        
        print('access_token', resource_owner_key)
        print('access_secret', resource_owner_secret)
    except Exception as e:
        print(e.__class__.__name__)
        print(e)
        
        ret = 1
    
    return ret

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get access token.')
    args = parser.parse_args()

    result = main(args)

    sys.exit(result)
