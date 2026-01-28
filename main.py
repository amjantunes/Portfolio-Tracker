from database import db_setup, get_tickers_earliest_transaction
from data_sourcing import get_stock_price

def main():
    connection = db_setup()
    if connection:
        print("Database connection successful.")
        
    values = get_tickers_earliest_transaction(connection)
    
    data = get_stock_price(values)
    print(data)
    
if __name__ == "__main__":
    main()

