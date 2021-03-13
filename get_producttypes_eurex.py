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

# GraphQL Script for querying product types available
query = '''query {
ProductInfos{
data {
  ProductType
}}}'''

# Key api info
api_header = { "X-DBP-APIKEY" : "68cdafd2-c5c1-49be-8558-37244ab4f513" }
url = 'https://api.developer.deutsche-boerse.com/prod/accesstot7-referencedata/1.1.0/'

# Post request to GraphQL API
results = requests.post(url, 
                  headers = api_header,
                  json={'query': query})

json_data = json.loads(results.text)

products = json_data['data']['ProductInfos']['data']

# Extract unique product types
df = pd.DataFrame(products).drop_duplicates(ignore_index = True)
print(df)