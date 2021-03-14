# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 14:26:45 2021

@author: Caddylee
"""

import warnings
warnings.filterwarnings('ignore')

import requests
import json
import pandas as pd

from datetime import date, datetime, timedelta

import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 500)

start = datetime.now()

################### USER INPUT ##########################
product_filter = ['FESX', 'FDAX', 'FDXM', 'FESB', 'FXXP', 'FVS',
                  'FGBL', 'FGBM', 'FGBS', 'FGBX', 'FOAT', 'FMK2',
                  'FBK2', 'OKS2']

################## API INFO ##########################
api_header = { "X-DBP-APIKEY" : "68cdafd2-c5c1-49be-8558-37244ab4f513" }
url = 'https://api.developer.deutsche-boerse.com/prod/accesstot7-referencedata/1.1.0/'

################## GRAPHQL SCRIPTS ##########################
query_productinfos = '''query {
TradingHours(filter: { Product: { eq: "%s" } }) {
date
data {
	Product,
	StartContinuosTrading,
  EndOpeningAuction,
	EndContinuosTrading,
	EndClosingAuction,
  StartTES,
  EndTES
}}}'''



################## GET ALL TRADING HOURS ##########################
for idx, prod in enumerate(product_filter ):
    
    # Post request to GraphQL API
    tradingHours_r = requests.post(url, 
                      headers = api_header,
                      json={'query': query_productinfos %(prod)})
    
    # Convert data format to JSON
    json_data = json.loads(tradingHours_r.text)
    
    # Extract data
    tradingHours = json_data['data']['TradingHours']['data']
    
    # Convert data to dataframe
    df_temp = pd.DataFrame(tradingHours)
    
    # Create and extend dataframe for all product required
    df_tradingHours  = df_temp.copy() if idx == 0 \
        else df_tradingHours.append(df_temp, ignore_index = True)

# Visualize the dataframe with trading hours info
print(df_tradingHours)

################# CONVERT TIMEZONE ###################################
schedule = ['StartContinuosTrading', 'EndOpeningAuction',
       'EndContinuosTrading', 'EndClosingAuction', 'StartTES', 'EndTES']

for item in schedule:
    df_tradingHours[item] = pd.to_timedelta(df_tradingHours[item])
    
# Simple method to convert timezone
if datetime.now() < datetime.strptime('28/03/2021', "%d/%m/%Y") \
    or datetime.now() > datetime.strptime('31/10/2021', "%d/%m/%Y"):
        original_timezone = 'CET'
        adjustment = timedelta(hours = 7)
else:
    original_timezone = 'CEST'
    adjustment = timedelta(hours = 6)

df_tradingHours_SGT = df_tradingHours.copy()

for item in schedule:
    df_tradingHours_SGT[item] += adjustment

df_tradingHours['Timezone'] = original_timezone
df_tradingHours_SGT['Timezone'] = 'SGT'

df_tradingHours_SGT.to_csv('TradingHoursSGT_20210314.csv')
    
