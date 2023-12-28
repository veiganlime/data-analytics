import pandas as pd
import requests
import json
import yaml


yaml_file = open('api_key/api_config_cc.yml', 'r')
p = yaml.load(yaml_file, Loader=yaml.FullLoader)
api_key = p['api_key']


#data_limit = 1
#ticker = 'TWT'



def api_request(url):
    headers = {'authorization': 'Apikey ' + api_key,}
    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url)

    #print('Response Status Code:', response.status_code)

    blockchain_data_dict = json.loads(response.text)

    #print('Response Content:', response.text)
    #print('blockchain_data_dict:', blockchain_data_dict)


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
    #print(ticker_price_df)
    price = ticker_price_df.at[1, f'{ticker} price']
    #print(price)

    return(price)




