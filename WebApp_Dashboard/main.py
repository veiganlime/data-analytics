import pandas as pd
import requests
import json
import yaml
import sqlite3 as sql
import numpy as np

# get the api key
yaml_file = open('api_key/api_config_cc.yml', 'r')
p = yaml.load(yaml_file, Loader=yaml.FullLoader)
api_key = p['api_key']

# API requset 
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

def load_data():
    # Load the data from SQL database
    conn = sql.connect('data/Crypto.db') 
    df_sum = pd.read_sql_query("SELECT * FROM PORTFOLIO", conn)
    conn.close

    # Data preparation
    df_sum['TotalAmount'] = df_sum.groupby('Ticker')['Amount'].transform('sum')
    df_sum.rename(columns={'TotalAmount':'Quantity'}, inplace=True)

    pd.set_option('display.float_format', '{:.6f}'.format)
    df_prepeared = df_sum[['Ticker', 'Quantity']].drop_duplicates()
    tickers_to_drop = ['VTX', 'CITY', 'IONX']# Drop a few rows for now due to an issue with the market maker. In the future, try using API requests with another financial aggregator.
    df_prepeared = df_prepeared[~df_prepeared['Ticker'].isin(tickers_to_drop)]

    return df_prepeared, df_sum


def dca_calculation(data ,start_date, end_date, payment):
    stack = []
    total_spend = 0
    
    start_index = data.index.get_loc(str(start_date))
    end_index = data.index.get_loc(str(end_date))
    data = data[start_index:end_index]
    for price in data['Adj Close']:                
        amount = payment*100/price *0.01                
        stack.append(amount)
        total_spend+=payment
        
    avg_cost = total_spend/ sum(stack)
    cost_now = price * sum(stack)
    percentage = price / avg_cost
    result = abs(1 - percentage)    
    
    return total_spend , stack, avg_cost, price, cost_now, result

def nearest_datetime_value(items, pivot):

    time_diff = np.abs([date - pivot for date in items])

    return time_diff.argmin(0)



