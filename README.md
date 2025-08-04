# 📈 Algo-Trading System with ML & Automation

This is a Python-based mini algo-trading prototype that integrates technical analysis, machine learning, Google Sheets automation, and Telegram alerts.

---

## 🚀 Features

- ✅ Fetches daily stock data using Yahoo Finance (via `yfinance`)
- ✅ Implements RSI + Moving Average crossover trading strategy
- ✅ Backtests strategy over a defined period
- ✅ Predicts next-day price movement using Random Forest Classifier
- ✅ Sends alerts via Telegram for BUY/SELL signals
- ✅ Logs results (signals, trades, analytics) to Google Sheets
- ✅ Final system summary printed to console and Google Sheets

---

## 🧠 Strategy Logic

- **Buy Signal**: When RSI < 30 and 20-MA crosses above 50-MA
- **Sell Signal**: When RSI > 70 or 20-MA crosses below 50-MA
- Configurable via `config.py`

---

## 📁 Folder Structure

```
algo/
├── src/
│   ├── data_fetcher.py
│   ├── strategy.py
│   ├── ml_model.py
│   ├── sheets_manager.py
│   ├── telegram_bot.py
│   ├── main.py
├── config.py
├── requirements.txt
```

---

## ⚙️ Configuration

Edit `config.py` to set:
```python
STOCKS = ['SBIN.NS', 'TCS.NS', 'INFY.NS']
START_DATE = "2024-10-01"
END_DATE = "2025-08-03"
RSI_BUY_THRESHOLD = 30
RSI_SELL_THRESHOLD = 70
POSITION_SIZE = 0.3
INITIAL_CAPITAL = 100000
ML_TEST_SIZE = 0.3
ML_RANDOM_STATE = 42
```

---

## 🔧 Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add your `credentials.json` (for Google Sheets API) in `src/`
3. Run the system:
```bash
cd src
python main.py
```

---

## 📊 Output

- ✅ Terminal summary (P&L, trades, ML predictions)
- ✅ Google Sheet: Logs of signals, trades, win rate
- ✅ Telegram alerts for BUY/SELL and system summary

---

## 📹 Demo Videos

- 🎥 [Video 1: Strategy Explanation, Run & Outputs](#)

(Replace with your actual Google Drive or YouTube links)

---

## 📬 Contact

Project by **Dhrudeep Vaghasiya**  
**Algo-Trading System with ML & Automation** assignment.

---
