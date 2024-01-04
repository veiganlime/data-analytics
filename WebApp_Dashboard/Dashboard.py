import streamlit as st
import pandas as pd
import numpy as np
import sqlite3 as sql
import main
import yfinance as yf
import plotly_express as px

st.sidebar.write("Select dashboard:")


st.write("This dashboard is still under deployement")
option = st.sidebar.selectbox(
    'Select dashboard',
    ('Porfolio owerview', 'Line chart', 'dashboard 3'))

if option == "Porfolio owerview":

    st.title("Portfolio overwiev")
    df_prepeared = main.load_data()
    st.dataframe(df_prepeared)
    plot = px.pie(df_prepeared, values='value', names='Ticker',title='Allocation',width=650, height=650 )
    st.plotly_chart(plot)


if option == "Line chart":
    
    input = st.text_input('Ticker:')
    ticker = f'{input}-USD'
    if len(input) > 0:
        start = st.date_input('Start', value = pd.to_datetime('2023-12-01'))
        end = st.date_input('End', value = pd.to_datetime('today'))
        df = yf.download(ticker, start, end)
        df = df.drop(columns=['Open', 'High', 'Low', 'Adj Close'])

        df.reset_index(inplace=True)
        df.rename(columns={'Close':'Price'}, inplace=True)
        df['Date'] = df['Date'].dt.strftime('%Y/%m/%d')    

        st.line_chart(
        df, x="Date", y=["Price"], color=["#FF0000"] 
        )
        st.line_chart(
        df, x="Date", y=["Volume"], color=["#0000FF"] 
        )
    else:
        st.write("Please enter the tickers value")


if option == "dashboard 3":
    
    st.title("This is the title 3")
    st.header("This is the header")
    st.write("This is a regular text")

    df = pd.DataFrame(np.random.randn(50,20), columns=('col %d' % i for i in range(20)))
    st.dataframe(df)