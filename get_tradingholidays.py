# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 00:54:17 2021

@author: Caddylee
"""

import warnings
warnings.filterwarnings('ignore')

import requests
import json
import pandas as pd

from datetime import date, datetime

import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 500)

start = datetime.now()

################### USER INPUT ##########################
type_filter = ['KOSPI','MSCI']
product_filter = ['FESX', 'FDAX', 'FDXM', 'FESB', 'FXXP', 'FVS',
                  'FGBL', 'FGBM', 'FGBS', 'FGBX', 'FOAT']

################## API INFO ##########################
api_header = { "X-DBP-APIKEY" : "68cdafd2-c5c1-49be-8558-37244ab4f513" }
url = 'https://api.developer.deutsche-boerse.com/prod/accesstot7-referencedata/1.1.0/'

################## GRAPHQL SCRIPTS ##########################
query_productinfos = '''query {
ProductInfos(filter: { Name: { contains: "%s" } }) {
date
data {
	Product,
	Name,
	ProductISIN,
	ProductLine,
  ProductType
}}}'''

query_holidays = '''query {
Holidays(filter: { Product: { eq: "%s"} }) {
date
data {
  Product,
  Holiday,
  ExchangeHoliday
}}}'''

################## GET DISTINCT PRODUCT CODES ##########################
for idx, prod_type in enumerate(type_filter):
    
    # Post request to GraphQL API
    products_r = requests.post(url, 
                      headers = api_header,
                      json={'query': query_productinfos %(prod_type)})
    
    # Convert data format to JSON
    json_data = json.loads(products_r.text)
    
    # Extract data
    product_suite = json_data['data']['ProductInfos']['data']
    
    # Convert data to dataframe
    df_temp = pd.DataFrame(product_suite)
    
    # Create and extend dataframe for all product types required
    df_product_suite  = df_temp.copy() if idx == 0 \
        else df_product_suite.append(df_temp, ignore_index = True)

# Visualize the dataframe with product information
print(df_product_suite)

# Expand target products for trading holiday retrieval
target_prods = product_filter + list(df_product_suite.iloc[:,0])

################## RETRIEVE TRADING HOLIDAYS ##########################
for idx, prod in enumerate(target_prods):
    print('Retrieving trading holidays for %s...'%prod)
    try:
        # Operation is similar to earlier post request
        holidays_r = requests.post(url, 
                                   headers = api_header,
                                   json={'query': query_holidays %(prod)})
    
        json_data = json.loads(holidays_r.text)
    
        holidays= json_data['data']['Holidays']['data']
        df_temp = pd.DataFrame(holidays)
        df_holidays  = df_temp.copy() if idx == 0 \
            else df_holidays.append(df_temp, ignore_index = True)
    except:
        print('Error encountered! product %s not found!' %prod)
        continue

print(df_holidays)        

# Convert 'Holiday' column data to datetime to ensure dates were sorted in chronological order
df_holidays['Holiday'] = pd.to_datetime(df_holidays['Holiday'], format = '%Y-%m-%d')

# Create matrix
holidays_matrix = pd.crosstab(df_holidays['Holiday'], df_holidays['Product'])

# Revert date back to string
holidays_matrix.index = holidays_matrix.index.astype(str)

# Extract data into CSV
today = date.today()
d1 = today.strftime('%Y%m%d')

holidays_matrix.to_csv('EurexTradingHolidays_{}.csv'.format(d1))

################## PLOT CALENDAR MATRIX ##########################

# Select a sample of 18 products for visualization purpose
sample = ['OKS2', 'FMK2', 'FBK2', 'FESX', 'FXXP', 'FGBL', 'FOAT',\
          'FMEA', 'FMCN', 'FMJP', 'FMIN', 'OMEA', 'OMCN', 'FVS',\
          'FDAX', 'FDXM', 'FESB', 'IDEM']

# Plot heatmap
fig, ax = plt.subplots(figsize=(11, 9))
sns.heatmap(holidays_matrix.loc[:,sample],cmap="YlGnBu")
plt.show()

print('Total process time %s seconds!'%(datetime.now() - start).seconds)