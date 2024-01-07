import streamlit as st
import pandas as pd
import numpy as np
import main
import yfinance as yf
import plotly_express as px
import sqlite3 as sql

st.sidebar.write("<h1>WebApp - Igor</h1>", unsafe_allow_html=True)
st.write("This dashboard is under deployement")
option = st.sidebar.selectbox(
    'Select dashboard',
    ('Porfolio owerview', 'Line chart', 'DCA Calculator', 'Data base'))

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
    # Users Values input
    st.title("Dollar cost average Calculator")
    input = st.text_input('Ticker:')
    ticker = f'{input}-USD'
    payment_str = st.text_input('Purchase amount in $:')    
    purchase_period = st.selectbox(
    'Purchase period:',
    ('Daily', 'Weekly', 'Monthly'))

    start_period = st.date_input('Start', value = pd.to_datetime('2023-01-01'))
    end_period = st.date_input('End', value = pd.to_datetime('today'))
    

    # Check, the period of investment strategy, and passing the stock dataframe and the date
    if purchase_period == 'Daily':
        stock_data = yf.download(tickers=ticker, period = 'max', interval = '1d')
        closest_start_date = start_period
        closest_end_date = end_period
    elif purchase_period == 'Monthly':   
        stock_data = yf.download(tickers=ticker, period = 'max', interval = '1d')
        if stock_data.index.min() <= pd.to_datetime(start_period) <= stock_data.index.max():
            stock_data = stock_data.resample('M').mean()

            start_period = pd.to_datetime(start_period)
            closest_start_date_index = main.nearest_datetime_value(stock_data.index, start_period)
            closest_start_date = stock_data.index[closest_start_date_index]

            end_period = pd.to_datetime(end_period)
            closest_end_date_index = main.nearest_datetime_value(stock_data.index, end_period)
            closest_end_date = stock_data.index[closest_end_date_index]
        else: 
            st.write("Error 1 - Please contact your developer team")
    elif purchase_period == 'Weekly':
        stock_data = yf.download(tickers=ticker, period = 'max', interval = '1d')
        if stock_data.index.min() <= pd.to_datetime(start_period) <= stock_data.index.max():
            stock_data = stock_data.resample('W').mean()

            start_period = pd.to_datetime(start_period)
            closest_start_date_index = main.nearest_datetime_value(stock_data.index, start_period)
            closest_start_date = stock_data.index[closest_start_date_index]

            end_period = pd.to_datetime(end_period)
            closest_end_date_index = main.nearest_datetime_value(stock_data.index, end_period)
            closest_end_date = stock_data.index[closest_end_date_index]
        else:
            st.write("Error 2- Please contact your developer team")


    if len(input) & len(payment_str) > 0:
        payment = float(payment_str)
        if stock_data.index.min() <= pd.to_datetime(closest_start_date) <= stock_data.index.max():
            total_spend , stack, avg_cost, price, cost_now, result  = main.dca_calculation(stock_data,closest_start_date, closest_end_date, payment)
            total_pofit = cost_now - total_spend

            formatted_total_pofit = f"Total pofit:  ${total_pofit:.2f}"
            formatted_total_spend = f"Total spend:  ${total_spend:.2f}"
            formatted_cost_now = f"Cost today:  ${cost_now:.2f}"

            # display outputs
            container = st.container(border=True)
            container.write(formatted_total_spend)
            container.divider()
            container.write(formatted_cost_now)
            container.divider()
            container.write(formatted_total_pofit)

        #Error handling
        else:
            first_date_in_dataframe = stock_data.index.date[0]
            input_upper = input.upper()
            error_message =  f"Your start date is not present in the date range for {input_upper} coin. Please change the start date value. The first available date is {first_date_in_dataframe} "
            st.divider()
            st.write(error_message)
            st.divider()
     #Error handling
    elif len(input) == 0:
        st.write("Please enter the tickers value!")
    #Error handling
    elif len(payment_str) == 0:
        st.write("Please add a Purchase amount!")

if option == "Data base":

    option2 = st.sidebar.selectbox(
    'Select an option:',
    ('Show data base', 'Add a new record', 'Delete a record'))

    if option2 == "Show data base":

        with st.form(key='input', clear_on_submit=True):

            btnResult = st.form_submit_button('Display all rows from data base')

            if btnResult:
                conn = sql.connect('data/test.db')
                df_sql = pd.read_sql_query("SELECT * FROM PORTFOLIO", conn)
                st.table(df_sql)
                conn.close()

    if option2 == "Add a new record":

        st.write("Insert a new record into a database")

        with st.form(key='input', clear_on_submit=True):

            st.write("For the database record, the following data are required: ticker, amount, date, price.")

            ticker = st.text_input(label="Ticker:", label_visibility="visible")
            amount = st.text_input(label="Amount:", label_visibility="visible")
            buy_date = st.text_input(label="Buy date:", label_visibility="visible")
            sell_date = st.text_input(label="Sell date:", label_visibility="visible")
            buy_price = st.text_input(label="Buy price:", label_visibility="visible")
            sell_price = st.text_input(label="Sell price:", label_visibility="visible")

            btnResult = st.form_submit_button('Execute')
            

        if btnResult:
            if len(ticker) > 0:
                if len(amount) >0:
                
                    st.text('Query executed')

                    conn = sql.connect('data/test.db')

                    with conn:
                        create_table_query = '''CREATE TABLE IF NOT EXISTS PORTFOLIO
                                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Ticker           TEXT    NOT NULL,
                                Amount           INT     NOT NULL,
                                BuyDate          INT     NOT NULL,
                                SellDate         INT     NOT NULL,
                                BuyPrice         INT     NOT NULL ,
                                SellPrice        INT     NOT NULL)'''
                        
                        insert_query = '''
                            INSERT INTO PORTFOLIO (Ticker, Amount, BuyDate, SellDate, BuyPrice, SellPrice)
                            VALUES (?, ?, ?, ?, ?, ?);'''
                        
                        # if the value is  NULL, then value should be 0.
                        buy_date = buy_date if buy_date else 0
                        sell_date = sell_date if sell_date else 0 
                        buy_price = buy_price if buy_price else 0
                        sell_price = sell_price if sell_price else 0

                        record_values = (ticker.upper(), amount, buy_date, sell_date, buy_price, sell_price)            
                        
                    
                        conn.execute(create_table_query)
                        conn.execute(insert_query, record_values)
                        # Load the data from SQL database
                        
                        df_sql = pd.read_sql_query("SELECT * FROM PORTFOLIO", conn)
                        st.table(df_sql)
                    
                    conn.commit()
                    conn.close()
                else:
                    st.text('Amount Error! - Please give the number of quantity!')
            else:
                st.text('Ticker Error! - Please give ticker name!')

    if option2 == "Delete a record":
         
        st.write("Delete a record from a database")

        with st.form(key='id', clear_on_submit=True):

            id = st.text_input(label="ID:", label_visibility="visible")
            btnResult = st.form_submit_button('Delete row from data base')

            if btnResult:
                conn = sql.connect('data/test.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM PORTFOLIO WHERE ID = ?", (id,))
                

                affected_rows = cursor.rowcount
                if affected_rows == 0:
                    st.write(f"No rows were deleted. Row with ID = {id} might not exist.")
                else:
                    st.write(f"Row with ID = {id} has been deleted successfully.")
                    conn.commit()

                df_sql = pd.read_sql_query("SELECT * FROM PORTFOLIO", conn)
                st.table(df_sql)
                conn.close()



        


