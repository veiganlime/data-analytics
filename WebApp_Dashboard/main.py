import pandas as pd
import requests
import json
import yaml

# get the api key
yaml_file = open('api_key/api_config_cc.yml', 'r')
p = yaml.load(yaml_file, Loader=yaml.FullLoader)
api_key = p['api_key']


def api_request(url):
    headers = {'authorization': 'Apikey ' + api_key,}
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url)
    blockchain_data_dict = json.loads(response.text)
    df = pd.DataFrame.from_dict(blockchain_data_dict.get('Data').get('Data'), orient='columns', dtype=None, columns=None)
    return(df)

def prepare_pricedata(df):
    df['date'] = pd.to_datetime(df['time'], unit='s')
    df.drop(columns=['time', 'conversionType', 'conversionSymbol','high', 'low', 'open', 'volumefrom', 'volumeto', 'date'], inplace=True)   
    return df

def get_price(ticker):
    data_limit = 1
    base_url = 'https://min-api.cryptocompare.com/data/v2/histoday?fsym='
    df_ticker = api_request(f'{base_url}{ticker}&tsym=USD&limit={data_limit}')
    ticker_price_df = prepare_pricedata(df_ticker)
    ticker_price_df = ticker_price_df.drop(0)
    ticker_price_df = ticker_price_df.rename(columns={'close': f'{ticker} price'})
    price = ticker_price_df.at[1, f'{ticker} price']
    return(price)




