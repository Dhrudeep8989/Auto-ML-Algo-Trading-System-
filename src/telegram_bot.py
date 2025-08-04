# src/telegram_bot.py

import requests
from datetime import datetime
import config

class TelegramBot:
    """Handle Telegram notifications"""
    
    def __init__(self):
        self.bot_token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.enabled = bool(self.bot_token and self.chat_id)
        
        if self.enabled:
            print("📱 Telegram bot enabled")
        else:
            print("📱 Telegram bot disabled (optional)")
    
    def send_message(self, message):
        """Send message to Telegram"""
        if not self.enabled:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            print(f"⚠️ Telegram error: {str(e)}")
            return False
    
    def send_signal_alert(self, signal):
        """Send trading signal alert"""
        if not self.enabled or signal['Signal'] == 'HOLD':
            return
        
        emoji = "🚀" if signal['Signal'] == 'BUY' else "💰"
        
        message = f"""
{emoji} <b>TRADING SIGNAL</b> {emoji}

<b>Stock:</b> {signal['Symbol']}
<b>Signal:</b> {signal['Signal']}
<b>Price:</b> ₹{signal['Price']:.2f}
<b>RSI:</b> {signal['RSI']:.1f}

<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}
        """
        
        self.send_message(message.strip())
    
    def send_summary(self, summary_data):
        """Send daily summary"""
        if not self.enabled:
            return
        
        total_pnl = summary_data.get('total_pnl', 0)
        status = "🟢" if total_pnl > 0 else "🔴" if total_pnl < 0 else "⚪"
        
        message = f"""
📊 <b>TRADING SUMMARY</b> 📊

<b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}
<b>Stocks:</b> {summary_data.get('stocks_count', 0)}
<b>Total Trades:</b> {summary_data.get('total_trades', 0)}
<b>Total P&L:</b> {status} ₹{total_pnl:.2f}

<b>ML Accuracy:</b> {summary_data.get('ml_accuracy', 'N/A')}
<b>Active Signals:</b> {summary_data.get('active_signals', 0)}
        """
        
        self.send_message(message.strip())
    
    def send_error(self, error_msg):
        """Send error alert"""
        if not self.enabled:
            return
        
        message = f"""
🚨 <b>SYSTEM ERROR</b> 🚨

<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}
<b>Error:</b> {error_msg[:200]}
        """
        
        self.send_message(message.strip())