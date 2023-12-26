import streamlit as st
import pandas as pd
import numpy as np
import sqlite3 as sql

import test

st.sidebar.write("This is the sidebar")



option = st.sidebar.selectbox(
    'Select dashboard',
    ('Owerview', 'dashboard 2', 'dashboard 3'))

if option == "Owerview":

    st.title("This is the title 1")
    st.header("This is the header")
    st.write("This is a regular text")

    conn = sql.connect('data/Crypto.db')
    
    df = pd.read_sql_query("SELECT * FROM PORTFOLIO", conn)
    df = df.drop(columns=['ID'])
    st.dataframe(df)
    st.dataframe(test.df_sum_1)

if option == "dashboard 2":
    
    st.title("This is the title 2")
    st.header("This is the header")
    st.write("This is a regular text")

    df = pd.DataFrame(np.random.randn(50,20), columns=('col %d' % i for i in range(20)))
    st.dataframe(df)

if option == "dashboard 3":
    
    st.title("This is the title 3")
    st.header("This is the header")
    st.write("This is a regular text")

    df = pd.DataFrame(np.random.randn(50,20), columns=('col %d' % i for i in range(20)))
    st.dataframe(df)