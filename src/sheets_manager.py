# src/sheets_manager.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import config

class SheetsManager:
    """Manage Google Sheets integration"""
    
    def __init__(self):
        self.client = None
        self.spreadsheet = None
        self.setup_connection()
    
    def setup_connection(self):
        """Setup Google Sheets connection"""
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                'credentials.json', scope
            )
            self.client = gspread.authorize(credentials)
            
            # Open or create spreadsheet
            try:
                self.spreadsheet = self.client.open(config.SPREADSHEET_NAME)
                print("✅ Connected to existing Google Sheets")
            except gspread.SpreadsheetNotFound:
                try:
                    self.spreadsheet = self.client.create(config.SPREADSHEET_NAME)
                    print("✅ Created new Google Spreadsheet")
                except Exception as create_error:
                    print(f"⚠️  Cannot create spreadsheet: {str(create_error)}")
                    print("   Possible causes: Drive storage full, permissions issue")
                    print("   Google Sheets logging will be disabled")
                    self.client = None
                    return
                    
        except FileNotFoundError:
            print("⚠️  credentials.json not found - Google Sheets disabled")
            self.client = None
        except Exception as e:
            print(f"⚠️  Google Sheets error: {str(e)}")
            print("   Google Sheets logging will be disabled")
            self.client = None
    
    def log_signals(self, signals):
        """Log current signals to Trade Log sheet"""
        if not self.client:
            return
        
        try:
            # Get or create Trade Log worksheet
            try:
                ws = self.spreadsheet.worksheet('Trade Log')
            except gspread.WorksheetNotFound:
                ws = self.spreadsheet.add_worksheet(title='Trade Log', rows=1000, cols=10)
                headers = ['Date', 'Symbol', 'Signal', 'Price', 'RSI', 'MA_20', 'MA_50']
                ws.append_row(headers)
            
            # Log each signal
            for signal in signals:
                if signal['Signal'] in ['BUY', 'SELL']:  # Only log actionable signals
                    row = [
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        signal['Symbol'],
                        signal['Signal'],
                        f"{signal['Price']:.2f}",
                        f"{signal['RSI']:.2f}",
                        f"{signal['MA_20']:.2f}",
                        f"{signal['MA_50']:.2f}"
                    ]
                    ws.append_row(row)
            
            print("✅ Signals logged to Google Sheets")
            
        except Exception as e:
            print(f"❌ Error logging signals: {str(e)}")
    
    def log_backtest_results(self, results_dict):
        """Log backtest results to Summary P&L sheet"""
        if not self.client:
            return
        
        try:
            # Get or create Summary worksheet
            try:
                ws = self.spreadsheet.worksheet('Summary P&L')
            except gspread.WorksheetNotFound:
                ws = self.spreadsheet.add_worksheet(title='Summary P&L', rows=100, cols=8)
                headers = ['Symbol', 'Total_Trades', 'Win_Rate', 'Total_PnL', 'Total_Return']
                ws.append_row(headers)
            
            # Log results for each stock
            for symbol, result in results_dict.items():
                if result:
                    row = [
                        result['symbol'],
                        result['total_trades'],
                        f"{result['win_rate']:.1%}",
                        f"₹{result['total_pnl']:.2f}",
                        f"{result['total_return']:.2f}%"
                    ]
                    ws.append_row(row)
            
            print("✅ Backtest results logged to Google Sheets")
            
        except Exception as e:
            print(f"❌ Error logging backtest results: {str(e)}")
    
    def log_analytics(self, analytics_data):
        """Log analytics to Win Ratio sheet"""
        if not self.client:
            return
        
        try:
            # Get or create Win Ratio worksheet
            try:
                ws = self.spreadsheet.worksheet('Win Ratio')
            except gspread.WorksheetNotFound:
                ws = self.spreadsheet.add_worksheet(title='Win Ratio', rows=100, cols=6)
                headers = ['Date', 'Total_Signals', 'Buy_Signals', 'Sell_Signals', 'ML_Accuracy']
                ws.append_row(headers)
            
            # Log analytics
            row = [
                datetime.now().strftime('%Y-%m-%d'),
                analytics_data.get('total_signals', 0),
                analytics_data.get('buy_signals', 0),
                analytics_data.get('sell_signals', 0),
                analytics_data.get('ml_accuracy', 'N/A')
            ]
            ws.append_row(row)
            
            print("✅ Analytics logged to Google Sheets")
            
        except Exception as e:
            print(f"❌ Error logging analytics: {str(e)}")
    
    def get_sheet_url(self):
        """Get spreadsheet URL"""
        if self.spreadsheet:
            return self.spreadsheet.url
        return None