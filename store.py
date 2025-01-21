import yfinance as yf
import pandas as pd
import numpy as np

def store_data(start_date, end_date, shift_europe=False):
    """
    Fetches daily market data for Japan, Europe, North America,
    computes daily log-returns, and applies shift logic to align
    them to a chosen reference day (usually the US close).
    
    :param shift_europe: bool, whether to shift Europe by -1 day.
    """
    tickers = {
        "^GSPC": "USA",        
        "^GSPTSE": "Canada",    
        "^FTSE": "UK",          
        "^FCHI": "France",      
        "^GDAXI": "Germany",    
        "FTSEMIB.MI": "Italy",
        "^N225": "Japan"
    }

    print(f"Fetching daily data from {start_date} to {end_date}...")
    data = yf.download(
        list(tickers.keys()),
        start=start_date,
        end=end_date,
        group_by="ticker",
        auto_adjust=True
    )

    if data.empty:
        print("No data returned. Check your date range or tickers.")
        return

    print("Computing daily log-returns and applying shifts...")

    log_returns = {}

    for ticker, country in tickers.items():
        closes = data[ticker]["Close"]
        # Daily log-returns
        returns = np.log(closes).diff()

        # Shift logic
        if country == "Japan":
            # shift by -1
            returns = returns.shift(0)
        elif country in ["UK", "France", "Germany", "Italy"] and shift_europe:
            # shift by -1 if shift_europe is True
            returns = returns.shift(-1)
        else:
            # USA, Canada => no shift
            returns = returns.shift(0)

        log_returns[country] = returns

    df = pd.DataFrame(log_returns)
    df.dropna(inplace=True)
    df.to_csv("aligned_data.csv")
    print("Aligned data saved to 'aligned_data.csv'")
