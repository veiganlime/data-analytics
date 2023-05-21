import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
from datetime import date, timedelta, datetime
import seaborn as sns
#import cryptocompare as cc
import requests
#import IPython
import yaml
import json

yaml_file = open('api_key/api_config_cc.yml', 'r')
p = yaml.load(yaml_file, Loader=yaml.FullLoader)
api_key = p['api_key']

data_limit = 2000

btc = 'BTC'
eth = 'ETH'

def api_request(url):
    headers = {'authorization': 'Apikey' + api_key} 
    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url)

    blockchain_data_dict = json.loads(response.text)

    df = pd.DataFrame.from_dict(blockchain_data_dict.get('Data').get('Data'), orient='columns', dtype=None,columns=None)

    return(df)
def prepare_pricedata(df):
    df['date'] = pd.to_datetime(df['time'], unit='s')
    df.drop(columns=['time', 'conversionType', 'conversionSymbol'], inplace=True)
    return df

base_url = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsym='
df_btc = api_request(f'{base_url}{btc}&sym=USD&limit={data_limit}')
print(df_btc.head(3))

# btc_price_df = prepare_pricedata(df_btc)
# df_eth = api_request(f'{base_url}{eth}&sym=USD&limit={data_limit}')
# eth_price_df = prepare_pricedata(df_eth)
# print(eth_price_df.head(3))