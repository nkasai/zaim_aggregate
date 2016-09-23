#!/bin/env python3
# -*- coding: UTF-8 -*-
'''
Created on 2016/09/22

@author: nkasai
'''
import sys
import argparse
from datetime import date
import requests
from requests_oauthlib.oauth1_auth import OAuth1

ZAIM_BASE_URL = 'https://api.zaim.net'
ZAIM_URL_MONEY_READ = '{}{}'.format(ZAIM_BASE_URL, '/v2/home/money')

CONSUMER_KEY = 'enter your consumer key'
CONSUMER_SECRET = 'enter your consumer secret'
ACCESS_TOKEN = 'enter your access token'
ACCESS_SECRET = 'enter your access secret'

YEAR = date.today().year   # this year

def main(args):
    """
    main
    """
    ret = 0
    
    try:
        oauth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
        
        year = YEAR if not args.year else args.year
        
        total_year = 0
        for month in list(range(1, 12)):
            target_start_date = '{0}-{1:02d}-01'.format(year, month)
            target_end_date = '{0}-{1:02d}-31'.format(year, month)
            
            #print('target_start_date', target_start_date)
            #print('target_end_date', target_end_date)
            
            total_month = 0
            page = 1
            while True:
                params = {
                    'mapping': 1,
                    'mode': 'payment',
                    'start_date': target_start_date,
                    'end_date': target_end_date,
                    'page': page,
                    'limit': 100,
                }
                r = requests.get(ZAIM_URL_MONEY_READ, params=params, auth=oauth)
                parsed = r.json()
                
                #print(r.url)
                #print(r.status_code)
                #print(r.headers)
                #print(parsed)
                
                money = parsed['money']
                
                if money:
                    page += 1
                    for row in money:
                        total_month += int(row['amount'])
                else:
                    break
            
            print('{0}-{1:02d} total: {2}'.format(year, month, total_month))
            total_year += total_month
            
        print('{} total: {}'.format(year, total_year))
        print('{} total average: {}'.format(year, total_year / 12))
    except Exception as e:
        print(e.__class__.__name__)
        print(e)
        
        ret = 1
    
    return ret

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='aggregate zaim data.')
    parser.add_argument('--year')
    args = parser.parse_args()

    result = main(args)

    sys.exit(result)
