# store.py
import yfinance as yf
import pandas as pd
import numpy as np

def store_data(start_date, end_date, shift_europe=False):
    """
    Retrieves daily market data for multiple regions,
    calculates daily log-returns, and applies a shift logic
    to align returns to a reference date (usually the US close).
    
    :param shift_europe: bool, indicates whether to shift European data by one day (-1).
    """
    tickers = {
        "^GSPC": "USA",        # S&P 500
        "^GSPTSE": "Canada",    # S&P/TSX Composite
        "^FTSE": "UK",          # FTSE 100
        "^FCHI": "France",      # CAC 40
        "^GDAXI": "Germany",    # DAX 40
        "FTSEMIB.MI": "Italy",  # FTSE MIB
        "^N225": "Japan"        # Nikkei 225
    }

    print(f"Fetching data from {start_date} to {end_date}...")

    data = yf.download(
        list(tickers.keys()),
        start=start_date,
        end=end_date,
        group_by="ticker",
        auto_adjust=True
    )

    if data.empty:
        print("No data retrieved. Check the date range or tickers.")
        return

    print("Computing log-returns and applying shifts...")

    log_returns = {}

    for ticker, country in tickers.items():
        closes = data[ticker]["Close"]
        # Compute daily log-returns
        returns = np.log(closes).diff()

        # Apply shifts to align returns
        if country == "Japan":
            # No shift for Japan in this example (or adjust if necessary)
            returns = returns.shift(0)
        elif country in ["UK", "France", "Germany", "Italy"] and shift_europe:
            # Shift European data by -1 day if requested
            returns = returns.shift(0)
        else:
            # No shift for USA and Canada
            returns = returns.shift(0)

        log_returns[country] = returns

    df = pd.DataFrame(log_returns)
    df.dropna(inplace=True)
    df.to_csv("aligned_data.csv")
    print("Aligned log-returns have been saved in 'aligned_data.csv'")
