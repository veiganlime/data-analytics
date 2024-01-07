import sqlite3


def create_table(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS TOKENSINFO
                                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Ticker               TEXT    NOT NULL,
                                Information          TEXT     NOT NULL
                                )''')


def main():
    conn = sqlite3.connect('data/Crypto.db')

    create_table(conn)

    conn.close()

if __name__ == "__main__":
    main()