import sqlite3 as sql
import pandas as pd 

conn = sql.connect('data/Crypto.db')

df_sum = pd.read_sql_query("SELECT * FROM PORTFOLIO", conn)
df_sum = df_sum.drop(columns=['ID'])

print(df_sum)



# Calculate the total amount for each ticker
df_sum['TotalAmount'] = df_sum.groupby('Ticker')['Amount'].transform('sum')

pd.set_option('display.float_format', '{:.6f}'.format)

# Display the result
df_sum_1 = df_sum[['Ticker', 'TotalAmount']].drop_duplicates()

print(df_sum_1)

