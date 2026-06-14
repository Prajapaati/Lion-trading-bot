import ccxt
from strategy import check_signals

# CoinDCX connection (Keys GitHub Secrets se aayengi)
import os
exchange = ccxt.coindcx({
    'apiKey': os.environ.get('API_KEY'),
    'secret': os.environ.get('SECRET_KEY'),
})

def run_bot():
    print("Engine Starting...")
    # Market se data lao
    ticker = exchange.fetch_ticker('BTC/INR') 
    
    # Strategy file se check karo
    decision = check_signals(ticker)
    
    if decision == "BUY":
        print("Signal: BUY Detected!")
        # exchange.create_market_buy_order('BTC/INR', amount)
    else:
        print("Status: Waiting for signal...")

if __name__ == "__main__":
    run_bot()
