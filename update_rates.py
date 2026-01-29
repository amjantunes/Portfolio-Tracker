import yfinance as yf
import psycopg2
import os
from datetime import datetime

def populate_exchange_rates():
    DB_URL = os.environ.get('DATABASE_URL')
    
    if not DB_URL:
        raise ValueError("DATABASE_URL was not found! Check your GitHub Secrets.")
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # Gets last date in DB 
    cur.execute("SELECT MAX(rate_date) FROM exchange_rates")
    last_date_in_db = cur.fetchone()[0]

    # If the table is empty gets the date of my first transaction
    if last_date_in_db is None:
        start_date = "2023-09-18"
    else:
        # Gets the day before the last date
        start_date = last_date_in_db.strftime('%Y-%m-%d')

    print(f"A descarregar dados desde: {start_date}")

    # EUR/USD ratio download 
    ticker = "EURUSD=X"
    data = yf.download(ticker, start=start_date)

    # Bulk insert
    for date, row in data.iterrows():
        rate_val = float(row['Close'])
        date_str = date.strftime('%Y-%m-%d')
        
        cur.execute("""
            INSERT INTO exchange_rates (rate_date, currency_pair, rate)
            VALUES (%s, 'EURUSD', %s)
            ON CONFLICT (rate_date) DO NOTHING;
        """, (date_str, rate_val))

    conn.commit()
    cur.close()
    conn.close()
    print("The exchange_rates db was successfuly updated!")

if __name__ == "__main__":
    populate_exchange_rates()