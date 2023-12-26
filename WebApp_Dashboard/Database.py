import sqlite3


def create_table(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS PORTFOLIO
        (ID INT PRIMARY KEY     NOT NULL,
        Ticker           TEXT    NOT NULL,
        Amount           INT     NOT NULL,
        BuyDate          INT     NOT NULL,
        SellDate         INT     NOT NULL,
        BuyPrice         INT     NOT NULL ,
        SellPrice        INT     NOT NULL)''')


def main():
    conn = sqlite3.connect('data/Crypto.db')

    create_table(conn)

    conn.close()

if __name__ == "__main__":
    main()