import psycopg2
import os
import yfinance as yf
import logging
from datetime import datetime

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def populate_exchange_rates():
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        logger.error("DATABASE_URL environment variable is missing.")
        raise EnvironmentError("DATABASE_URL not found. Check your GitHub Secrets.")

    conn = None
    try:
        # Connect to Database
        logger.info("Connecting to the database...")
        conn = psycopg2.connect(db_url, connect_timeout=10)
        cur = conn.cursor()

        #Check the last recorded date
        logger.info("Checking for the latest rate date in the database...")
        cur.execute("SELECT MAX(rate_date) FROM exchange_rates")
        last_date_in_db = cur.fetchone()[0]

        #Define the start date
        if last_date_in_db is None:
            start_date = "2023-09-18"
            logger.info(f"Database is empty. Using default start date: {start_date}")
        else:
            start_date = last_date_in_db.strftime('%Y-%m-%d')
            logger.info(f"Last record found: {start_date}")

        # Download data
        ticker = "EURUSD=X"
        logger.info(f"Downloading {ticker} data from {start_date}...")
        data = yf.download(ticker, start=start_date)

        if data.empty:
            logger.warning("No new data found on Yahoo Finance.")
        else:
            # Bulk insert data
            logger.info(f"Processing {len(data)} rows...")
            inserted_count = 0
            
            for date, row in data.iterrows():
                if row.empty or 'Close' not in row:
                    continue
                    
                rate_val = float(row.iloc[0])
                date_str = date.strftime('%Y-%m-%d')
                
                cur.execute("""
                    INSERT INTO exchange_rates (rate_date, currency_pair, rate)
                    VALUES (%s, 'EURUSD', %s)
                    ON CONFLICT (rate_date) DO NOTHING;
                """, (date_str, rate_val))
                
                if cur.rowcount > 0:
                    inserted_count += 1

            conn.commit()
            logger.info(f"Successfully updated: {inserted_count} new rows inserted.")

        cur.close()

    except Exception as e:
        # Log the error and then RE-RAISE it to trigger a GitHub Action failure
        logger.error(f"An error occurred during execution: {e}")
        if conn:
            conn.rollback()
        raise 

    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")

if __name__ == "__main__":
    populate_exchange_rates()