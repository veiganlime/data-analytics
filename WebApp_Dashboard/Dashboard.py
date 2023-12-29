import streamlit as st
import pandas as pd
import numpy as np
import sqlite3 as sql
import main
import yfinance as yf

st.sidebar.write("This is the sidebar")



option = st.sidebar.selectbox(
    'Select dashboard',
    ('Owerview', 'Line chart', 'dashboard 3'))

if option == "Owerview":

    st.title("Portfolio overwiev")

    conn = sql.connect('data/Crypto.db')    # SQL database connection
    df = pd.read_sql_query("SELECT * FROM PORTFOLIO", conn)
    df = df.drop(columns=['ID'])
    conn = sql.connect('data/Crypto.db')


    df_sum = pd.read_sql_query("SELECT * FROM PORTFOLIO", conn)
    df_sum = df_sum.drop(columns=['ID'])


    df_sum['TotalAmount'] = df_sum.groupby('Ticker')['Amount'].transform('sum')

    pd.set_option('display.float_format', '{:.6f}'.format)
    df_sum_1 = df_sum[['Ticker', 'TotalAmount']].drop_duplicates()
    tickers_to_drop = ['VTX', 'CITY', 'IONX']# Drop a few rows for now due to an issue with the market maker. In the future, try using API requests with another financial aggregator.
    df_sum_1 = df_sum_1[~df_sum_1['Ticker'].isin(tickers_to_drop)]
    values = []

    for index, row in df_sum_1.iterrows(): # Loop to calculate the current value of each coin.
        ticker = row['Ticker']
        total_amount = row['TotalAmount']
        price = main.get_price(ticker)# get_price function with API request.
        calculated_value = total_amount * price
        values.append(calculated_value)

    df_sum_1['value'] = values
    st.dataframe(df_sum_1)


if option == "Line chart":
    
    input = st.text_input('Ticker:')
    ticker = f'{input}-USD'
    if len(input) > 0:
        start = st.date_input('Start', value = pd.to_datetime('2023-12-01'))
        end = st.date_input('End', value = pd.to_datetime('today'))
        df = yf.download(ticker, start, end)
        df = df.drop(columns=['Open', 'High', 'Low', 'Adj Close', 'Volume'])

        df.reset_index(inplace=True)
        df['Date'] = df['Date'].dt.strftime('%Y/%m/%d')    

        st.line_chart(
        df, x="Date", y=["Close"], color=["#FF0000"] 
        )


if option == "dashboard 3":
    
    st.title("This is the title 3")
    st.header("This is the header")
    st.write("This is a regular text")

    df = pd.DataFrame(np.random.randn(50,20), columns=('col %d' % i for i in range(20)))
    st.dataframe(df)