# src/main.py - Main Controller for Algo Trading System

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
import config
from src.data_fetcher import DataFetcher
from src.strategy import TradingStrategy
from src.ml_model import MLPredictor
from src.sheets_manager import SheetsManager
from src.telegram_bot import TelegramBot

class AlgoTradingSystem:
    """Main Algo Trading System Controller"""
    
    def __init__(self):
        print("🚀 Initializing Algo Trading System")
        print("=" * 50)
        
        # Initialize components
        self.data_fetcher = DataFetcher()
        self.strategy = TradingStrategy()
        self.ml_predictor = MLPredictor()
        self.sheets_manager = SheetsManager()
        self.telegram_bot = TelegramBot()
        
        # Data storage
        self.stock_data = {}
        self.backtest_results = {}
        self.current_signals = []
        
        print("✅ System initialized\n")
    
    def fetch_all_data(self):
        """Fetch data for all stocks"""
        print("📊 STEP 1: DATA INGESTION")
        print("-" * 30)
        
        for symbol in config.STOCKS:
            data = self.data_fetcher.fetch_stock_data(symbol, config.START_DATE, config.END_DATE)
            if data is not None:
                # Generate trading signals
                data_with_signals = self.strategy.generate_signals(data, symbol)
                self.stock_data[symbol] = data_with_signals
        
        print(f"✅ Loaded data for {len(self.stock_data)} stocks\n")
        return len(self.stock_data) > 0
    
    def run_backtests(self):
        """Run backtests for all stocks"""
        print("🎯 STEP 2: STRATEGY BACKTESTING")
        print("-" * 35)
        
        for symbol, data in self.stock_data.items():
            result = self.strategy.backtest(data, symbol)
            if result:
                self.backtest_results[symbol] = result
        
        print(f"✅ Completed backtests for {len(self.backtest_results)} stocks\n")
        return len(self.backtest_results) > 0
    
    def train_ml_model(self):
        """Train machine learning model"""
        print("🤖 STEP 3: MACHINE LEARNING")
        print("-" * 28)
        
        model = self.ml_predictor.train_model(self.stock_data)
        
        if model:
            print(f"✅ ML model ready\n")
            return True
        else:
            print("⚠️  ML training failed\n")
            return False
    
    def analyze_current_market(self):
        """Analyze current market signals"""
        print("📊 STEP 4: CURRENT MARKET ANALYSIS")
        print("-" * 38)
        
        self.current_signals = self.strategy.get_current_signals(self.stock_data)
        
        # Add ML predictions
        for signal in self.current_signals:
            symbol = signal['Symbol']
            data = self.stock_data[symbol]
            latest = data.iloc[-1]
            
            features = [latest['RSI'], latest['MACD'], latest['Volume_Ratio'], 
                       latest['MA_20'], latest['MA_50']]
            
            ml_result = self.ml_predictor.predict(features)
            if ml_result:
                signal['ML_Prediction'] = ml_result['prediction']
                signal['ML_Confidence'] = ml_result['confidence']
        
        # Send Telegram alerts for BUY/SELL signals
        for signal in self.current_signals:
            if signal['Signal'] in ['BUY', 'SELL']:
                self.telegram_bot.send_signal_alert(signal)
        
        print(f"✅ Analyzed {len(self.current_signals)} signals\n")
        return True
    
    def log_to_sheets(self):
        """Log all results to Google Sheets"""
        print("📝 STEP 5: GOOGLE SHEETS LOGGING")
        print("-" * 35)
        
        # Log signals
        self.sheets_manager.log_signals(self.current_signals)
        
        # Log backtest results
        self.sheets_manager.log_backtest_results(self.backtest_results)
        
        # Log analytics
        buy_signals = len([s for s in self.current_signals if s['Signal'] == 'BUY'])
        sell_signals = len([s for s in self.current_signals if s['Signal'] == 'SELL'])
        
        analytics_data = {
            'total_signals': len(self.current_signals),
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'ml_accuracy': f"{self.ml_predictor.accuracy:.1%}" if self.ml_predictor.accuracy else 'N/A'
        }
        
        self.sheets_manager.log_analytics(analytics_data)
        
        print("✅ Results logged to Google Sheets\n")
        return True
    
    def print_summary(self):
        """Print comprehensive system summary"""
        print("=" * 60)
        print("           📊 ALGO TRADING SYSTEM SUMMARY")
        print("=" * 60)
        
        # Data Summary
        print(f"\n📈 DATA ANALYSIS:")
        print(f"   Period: {config.START_DATE} to {config.END_DATE}")
        print(f"   Stocks: {', '.join(config.STOCKS)}")
        
        # Backtest Results
        print(f"\n🎯 BACKTEST RESULTS:")
        total_trades = 0
        total_pnl = 0
        
        for symbol, result in self.backtest_results.items():
            print(f"   • {symbol}:")
            print(f"     - Trades: {result['total_trades']}")
            print(f"     - Win Rate: {result['win_rate']:.1%}")
            print(f"     - P&L: ₹{result['total_pnl']:.2f}")
            print(f"     - Return: {result['total_return']:.2f}%")
            total_trades += result['total_trades']
            total_pnl += result['total_pnl']
        
        # ML Results
        if self.ml_predictor.accuracy:
            print(f"\n🤖 MACHINE LEARNING:")
            print(f"   • Model: Random Forest")
            print(f"   • Accuracy: {self.ml_predictor.accuracy:.1%}")
        
        # Current Signals
        print(f"\n📊 CURRENT SIGNALS:")
        for signal in self.current_signals:
            emoji = {"BUY": "🟢", "SELL": "🔴", "HOLD": "⚪"}[signal['Signal']]
            print(f"   {emoji} {signal['Symbol']}: {signal['Signal']} at ₹{signal['Price']:.2f}")
            
            if 'ML_Prediction' in signal:
                ml_emoji = "📈" if signal['ML_Prediction'] == 'UP' else "📉"
                print(f"      {ml_emoji} ML: {signal['ML_Prediction']} ({signal['ML_Confidence']:.1%})")
        
        # Overall Performance
        print(f"\n💰 OVERALL PERFORMANCE:")
        print(f"   • Total Trades: {total_trades}")
        print(f"   • Total P&L: ₹{total_pnl:.2f}")
        print(f"   • Status: {'🟢 PROFITABLE' if total_pnl > 0 else '🔴 LOSS'}")
        
        # Google Sheets URL
        sheet_url = self.sheets_manager.get_sheet_url()
        if sheet_url:
            print(f"\n📋 Google Sheets: {sheet_url}")
        
        print("=" * 60)
    
    def run(self):
        """Execute the complete trading pipeline"""
        try:
            print("🚀 STARTING ALGO TRADING SYSTEM")
            print(f"📅 Period: {config.START_DATE} to {config.END_DATE}")
            print(f"📈 Stocks: {', '.join(config.STOCKS)}")
            print("=" * 50)
            
            # Execute all steps
            if not self.fetch_all_data():
                print("❌ Data fetching failed")
                return False
            
            if not self.run_backtests():
                print("❌ Backtesting failed") 
                return False
            
            self.train_ml_model()  # Optional, continues if fails
            
            self.analyze_current_market()
            
            self.log_to_sheets()
            
            # Send Telegram summary
            if self.telegram_bot.enabled:
                total_pnl = sum([r['total_pnl'] for r in self.backtest_results.values()])
                active_signals = len([s for s in self.current_signals if s['Signal'] != 'HOLD'])
                
                summary_data = {
                    'stocks_count': len(self.stock_data),
                    'total_trades': sum([r['total_trades'] for r in self.backtest_results.values()]),
                    'total_pnl': total_pnl,
                    'ml_accuracy': f"{self.ml_predictor.accuracy:.1%}" if self.ml_predictor.accuracy else 'N/A',
                    'active_signals': active_signals
                }
                
                self.telegram_bot.send_summary(summary_data)
            
            # Print final summary
            self.print_summary()
            
            print(f"\n✅ SYSTEM COMPLETED SUCCESSFULLY!")
            print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return True
            
        except Exception as e:
            error_msg = f"System error: {str(e)}"
            print(f"\n❌ {error_msg}")
            self.telegram_bot.send_error(error_msg)
            return False

def main():
    """Main function"""
    print("🏁 Algo Trading System with ML & Automation")
    print("=" * 50)
    
    system = AlgoTradingSystem()
    success = system.run()
    
    if success:
        print("\n🎉 Execution completed successfully!")
    else:
        print("\n❌ Execution failed - check logs above")

if __name__ == "__main__":
    main()