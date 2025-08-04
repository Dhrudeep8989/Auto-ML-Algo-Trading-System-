# # src/strategy.py

import pandas as pd
import numpy as np
import config

class TradingStrategy:
    """RSI + Moving Average crossover trading strategy"""
    
    def __init__(self):
        pass
    
    def generate_signals(self, data, symbol):
        """Generate buy/sell signals"""
        signals = data.copy()
        signals['Signal'] = 0  # 0: Hold, 1: Buy, -1: Sell
        
        # Buy: RSI < 30 AND 20-MA > 50-MA (with crossover)
        buy_condition = (
            (signals['RSI'] < config.RSI_BUY_THRESHOLD) &
            (signals['MA_20'] > signals['MA_50']) 
            #&(signals['MA_20'].shift(1) <= signals['MA_50'].shift(1))

            #(signals['RSI'] < 45) & (signals['MA_20'] > signals['MA_50'])
        )
        
        # Sell: RSI > 70 OR 20-MA < 50-MA (with crossover)
        sell_condition = (
            (signals['RSI'] > config.RSI_SELL_THRESHOLD) |
            ((signals['MA_20'] < signals['MA_50'])) 
            #&(signals['MA_20'].shift(1) >= signals['MA_50'].shift(1)))
            
            #(signals['RSI'] > 55) | (signals['MA_20'] < signals['MA_50'])
        )
        
        signals.loc[buy_condition, 'Signal'] = 1
        signals.loc[sell_condition, 'Signal'] = -1
        
        print(f"📈 {symbol}: {signals['Signal'].abs().sum()} signals generated")
        return signals
    
    def backtest(self, data_with_signals, symbol):
        """Backtest the strategy"""
        print(f"🔄 Backtesting {symbol}...")
        
        trades = []
        cash = config.INITIAL_CAPITAL
        shares = 0
        
        for date, row in data_with_signals.iterrows():
            current_price = row['Close']
            signal = row['Signal']
            
            if signal == 1 and shares == 0:  # Buy
                position_value = (cash + shares * current_price) * config.POSITION_SIZE
                shares_to_buy = int(position_value / current_price)
                
                if shares_to_buy > 0 and cash >= shares_to_buy * current_price:
                    shares = shares_to_buy
                    cash -= shares * current_price
                    entry_date = date
                    entry_price = current_price
            
            elif signal == -1 and shares > 0:  # Sell
                revenue = shares * current_price
                cash += revenue
                
                pnl = revenue - (shares * entry_price)
                pnl_percent = (pnl / (shares * entry_price)) * 100
                
                trades.append({
                    'Entry_Date': entry_date,
                    'Exit_Date': date,
                    'Entry_Price': entry_price,
                    'Exit_Price': current_price,
                    'Shares': shares,
                    'PnL': pnl,
                    'PnL_Percent': pnl_percent
                })
                shares = 0

        if not trades:
            print(f"⚠️ {symbol}: No trades executed during backtest period.")
            return None

        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['PnL'] > 0])
        win_rate = winning_trades / total_trades
        total_pnl = sum([t['PnL'] for t in trades])
        
        final_value = cash + shares * data_with_signals['Close'].iloc[-1]
        total_return = ((final_value - config.INITIAL_CAPITAL) / config.INITIAL_CAPITAL) * 100
        
        result = {
            'symbol': symbol,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'total_return': total_return,
            'trades': trades
        }
        
        print(f"✅ {symbol}: {total_trades} trades, {win_rate:.1%} win rate, ₹{total_pnl:.2f} P&L")
        return result
    
    def get_current_signals(self, data_dict):
        """Get current trading signals"""
        current_signals = []
        
        for symbol, data in data_dict.items():
            if data is not None and len(data) > 0:
                latest = data.iloc[-1]
                
                signal_info = {
                    'Symbol': symbol,
                    'Price': latest['Close'],
                    'RSI': latest['RSI'],
                    'MA_20': latest['MA_20'],
                    'MA_50': latest['MA_50'],
                    'Signal': 'HOLD'
                }
                
                if latest['Signal'] == 1:
                    signal_info['Signal'] = 'BUY'
                elif latest['Signal'] == -1:
                    signal_info['Signal'] = 'SELL'
                
                current_signals.append(signal_info)
        
        return current_signals
