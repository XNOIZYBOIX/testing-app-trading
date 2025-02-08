import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_historical_data(symbol, period='1mo'):
    """Fetch historical stock data from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        df = df.reset_index()
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    except Exception as e:
        raise ValueError(f"Error fetching data for {symbol}: {str(e)}")

def get_real_time_price(symbol):
    """Get real-time stock price"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d', interval='1m')
        if not data.empty:
            return data['Close'].iloc[-1]
        return None
    except Exception as e:
        raise ValueError(f"Error fetching real-time price for {symbol}: {str(e)}")

def update_dataset(symbol, days=30):
    """Update and save dataset for a stock"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)
        df.to_csv(f"data/{symbol}_latest.csv")
        return True
    except Exception as e:
        raise ValueError(f"Error updating dataset for {symbol}: {str(e)}")
