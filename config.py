# config.py - Configuration for Algo Trading System

import os
from datetime import datetime, timedelta

# Stock Selection (3 NIFTY 50 stocks as required)
STOCKS = ['SBIN.NS', 'TCS.NS', 'INFY.NS']

 #Date Range (6 months for backtesting) - FIXED FOR CURRENT DATE
END_DATE = datetime.today().strftime('%Y-%m-%d')
START_DATE = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')

# Trading Strategy Parameters
RSI_BUY_THRESHOLD = 30
RSI_SELL_THRESHOLD = 70
MA_SHORT_PERIOD = 20
MA_LONG_PERIOD = 50

# Portfolio Settings
INITIAL_CAPITAL = 100000
POSITION_SIZE = 0.1

# Google Sheets
SPREADSHEET_NAME = 'Algo Trading Results'

# ML Model Settings
ML_TEST_SIZE = 0.2
ML_RANDOM_STATE = 42

# Telegram Bot (Optional)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8288991098:AAFihAoHzV1_ipQbFjz5A9zeG8Ocv_pKM1I')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '1056600176')