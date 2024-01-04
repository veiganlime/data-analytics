import pandas as pd
import requests
import json
import yaml
import streamlit as st
import sqlite3 as sql

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

def load_data():

    conn = sql.connect('data/Crypto.db') # SQL database connection
    df_sum = pd.read_sql_query("SELECT * FROM PORTFOLIO", conn)
    df_sum = df_sum.drop(columns=['ID'])


    df_sum['TotalAmount'] = df_sum.groupby('Ticker')['Amount'].transform('sum')
    df_sum.rename(columns={'TotalAmount':'Quantity'}, inplace=True)

    pd.set_option('display.float_format', '{:.6f}'.format)
    df_prepeared = df_sum[['Ticker', 'Quantity']].drop_duplicates()
    tickers_to_drop = ['VTX', 'CITY', 'IONX']# Drop a few rows for now due to an issue with the market maker. In the future, try using API requests with another financial aggregator.
    df_prepeared = df_prepeared[~df_prepeared['Ticker'].isin(tickers_to_drop)]

    values = []
    for index, row in df_prepeared.iterrows(): # Loop to calculate the current value of each coin.
        ticker = row['Ticker']
        total_amount = row['Quantity']
        price = get_price(ticker)# get_price function with API request.
        calculated_value = total_amount * price
        values.append(calculated_value)

    df_prepeared['value'] = values
    # Total investment value calculation 
    df_sum['Amount'] = df_sum['Amount'].astype(float)
    df_sum['BuyPrice'] = df_sum['BuyPrice'].replace({',': ''}, regex=True).astype(float)
    df_sum['Invested Value'] = df_sum['Amount'] * df_sum['BuyPrice']
    

    total_invested_value = df_sum['Invested Value'].sum()
    formatted_sum_total_invested = f"Total Invested: ${total_invested_value:.2f}"    

    sum_value = df_prepeared['value'].sum()
    formatted_sum = f"The total holdings: ${sum_value:.2f}"

    unrealised_profit = sum_value - total_invested_value
    formatted_sum_unrealised_profit = f"Unrealised Profit:  ${unrealised_profit:.2f}"

    container = st.container(border=True)
    container.write(formatted_sum_total_invested)
    container.write(formatted_sum)
    container.write(formatted_sum_unrealised_profit)

    #st.write(formatted_sum)
    #st.write(formatted_sum_total_inested)


    return df_prepeared




