import yfinance as yf

def get_stock_price(values):
    
    results = {}
    
    for ticker, start_date in values:        
        print(f"Fetching {ticker} from {start_date}")

        try:
            stock = yf.Ticker(ticker)
            hist = (stock.history(start=start_date))
            
            if not hist.empty:
                results[ticker] = hist['Close']
            else : 
                print(f"No data found for {ticker}")
                results[ticker] = None
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            results[ticker] = None
            
    return results