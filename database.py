import psycopg2 as psy
from dotenv import load_dotenv
import os 
import logging

GET_EARLIEST_TRANSACTION_PER_TICKER = """
    SELECT ticker, transaction_date
        FROM (
            SELECT *,
                ROW_NUMBER() OVER (
                PARTITION BY ticker
                ORDER BY transaction_date ASC
            ) AS rn
        FROM transactions
    ) t
    WHERE rn = 1;"""

def db_setup():
    
    load_dotenv(".env")
    try:
        # Attempt to connect to the database
        db_url = os.environ.get("DATABASE_URL")
        conn = psy.connect(db_url)
        
        cur = conn.cursor()
        cur.fetchall
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_tickers_earliest_transaction(conn):
    
    cur = conn.cursor()
    cur.execute(GET_EARLIEST_TRANSACTION_PER_TICKER)
    values = cur.fetchall()
    
    return values
    

