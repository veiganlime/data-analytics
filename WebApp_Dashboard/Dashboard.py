import streamlit as st
import pandas as pd
import numpy as np
import main
import yfinance as yf
import plotly_express as px

st.sidebar.write("Select dashboard:")


st.write("This dashboard is still under deployement")
option = st.sidebar.selectbox(
    'Select dashboard',
    ('Porfolio owerview', 'Line chart', 'DCA Calculator'))

if option == "Porfolio owerview":

    st.title("Portfolio overwiev")
    df_prepeared, df_sum = main.load_data()

    values = []
    for index, row in df_prepeared.iterrows(): # Loop to calculate the current value of each coin.
        ticker = row['Ticker']
        total_amount = row['Quantity']
        price = main.get_price(ticker)# get_price function with API request.
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

    # display outputs
    container = st.container(border=True)
    container.write(formatted_sum_total_invested)
    container.divider()
    container.write(formatted_sum)
    container.divider()
    container.write(formatted_sum_unrealised_profit)
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


if option == "DCA Calculator":
    
    st.title("Dollar cost average Calculator")
    input = st.text_input('Ticker:')
    ticker = f'{input}-USD'
    payment_str = st.text_input('Purchase amount in $:')    
    RepeatePurchase = st.selectbox(
    'Repeate Purchase:',
    ('Daily', 'Weekly', 'Monthly'))

    if len(input) & len(payment_str) > 0:
        payment = float(payment_str)
        start_period = st.date_input('Start', value = pd.to_datetime('2023-01-01'))
        end_period = st.date_input('End', value = pd.to_datetime('today'))
        stock_data = yf.download(tickers=ticker, period = 'max', interval = '1d')

        if start_period in stock_data.index.date:       
            
            total_spend , stack, avg_cost, price, cost_now, result  = main.dca_calculation(stock_data,start_period, end_period, payment)

            formatted_total_spend = f"Total spend:  ${total_spend:.2f}"
            formatted_cost_now = f"Cost today:  ${cost_now:.2f}"

            # display outputs
            container = st.container(border=True)
            container.write(formatted_total_spend)
            container.divider()
            container.write(formatted_cost_now)

        else:
            first_date_in_dataframe = stock_data.index.date[0]
            input_upper = input.upper()
            error_message =  f"Your start date is not present in the date range for {input_upper} coin. Please change the start date value. The first available date is {first_date_in_dataframe} "
            st.divider()
            st.write(error_message)
            st.divider()

    elif len(input) == 0:
        st.write("Please enter the tickers value!")

    elif len(payment_str) == 0:
        st.write("Please add a Purchase amount!")
