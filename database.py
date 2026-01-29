import psycopg2 as psy
from dotenv import load_dotenv
import os 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    """
    Sets up the database connection using environment variables.
    Works for both local development (.env) and GitHub Actions (Secrets).
    """
    
    load_dotenv(".env")
    
    db_url = os.environ.get("DATABASE_URL")
    
    if not db_url:
        logger.error("DATABASE_URL variable not found in environment!")
        return None
    try:        
        logger.info("Attempting to connect to the database...")
        
        conn = psy.connect(db_url)
        logger.info("Database connection established successfully!")
        cur = conn.cursor()
        cur.fetchall
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        return None


def get_tickers_earliest_transaction(conn):
    """
    Fetches the first transaction date for each ticker in the database.
    """
    
    if conn is None:
        logger.warning("No active database connection found.")
        return []
    
    try:
        cur = conn.cursor()
        cur.execute(GET_EARLIEST_TRANSACTION_PER_TICKER)
        values = cur.fetchall()
        cur.close()
        return values
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        return []
    

