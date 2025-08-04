# # src/data_fetcher.py

import yfinance as yf
import pandas as pd
import numpy as np

class DataFetcher:
    """Handle stock data fetching and technical indicators"""
    
    def __init__(self):
        pass
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def fetch_stock_data(self, symbol, start_date, end_date):
        """Fetch stock data and add technical indicators"""
        try:
            print(f"📊 Fetching data for {symbol}...")
            
            # Download data
            stock = yf.Ticker(symbol)
            data = stock.history(start=start_date, end=end_date)
            
            if data.empty:
                print(f"❌ No data for {symbol}")
                return None
            
            # Add technical indicators
            data['RSI'] = self.calculate_rsi(data['Close'])
            data['MA_20'] = data['Close'].rolling(window=20).mean()
            data['MA_50'] = data['Close'].rolling(window=50).mean()
            
            # MACD for ML
            exp1 = data['Close'].ewm(span=12).mean()
            exp2 = data['Close'].ewm(span=26).mean()
            data['MACD'] = exp1 - exp2
            
            # Volume ratio
            data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
            data['Volume_Ratio'] = data['Volume'] / data['Volume_MA']
            
            # ML target
            data['Next_Day_Up'] = (data['Close'].shift(-1) > data['Close']).astype(int)
            
            # Drop rows with NaN in important ML fields
            data.dropna(subset=['RSI', 'MA_20', 'MA_50', 'MACD', 'Volume_Ratio', 'Next_Day_Up'], inplace=True)
            
            print(f"✅ {symbol}: {len(data)} data points")
            return data
            
        except Exception as e:
            print(f"❌ Error fetching {symbol}: {str(e)}")
            return None
