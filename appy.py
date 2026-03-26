import os, threading, time, random, pyotp
from flask import Flask, jsonify, request
from flask_cors import CORS
from SmartApi import SmartConnect
import yfinance as yf

app = Flask(__name__)
CORS(app)

# 🔐 YOUR BHARAT CREDENTIALS
API_KEY = "cROgNPxo"
CLIENT_ID = "AAAM840696" 
PASSWORD = "2580"   
TOTP_STR = "G6C2V5XZJNDS47VRS5YU6RXP6Q" 

bot_active = False
master_data = {
    "nifty": 0, "bank_nifty": 0, "price": 0, 
    "signal": "WAIT", "news": "Scanning Bharat Markets...", 
    "pumping_stocks": [], "logs": "Lion System Ready", "mood": 50
}

def bharat_scanner_logic():
    global master_data
    while True:
        try:
            # Live Nifty & Bank Nifty from NSE
            nifty = yf.download("^NSEI", period="1d", interval="1m", progress=False)
            bn = yf.download("^NSEBANK", period="1d", interval="1m", progress=False)
            
            master_data["nifty"] = round(nifty['Close'].iloc[-1], 2)
            master_data["bank_nifty"] = round(bn['Close'].iloc[-1], 2)
            master_data["price"] = master_data["nifty"]
            
            # Bharat Intelligence Update
            master_data["news"] = "FII buying observed in Indian Bluechips. Nifty Bullish."
            master_data["pumping_stocks"] = ["RELIANCE", "SBI", "TATASTEEL", "ADANIENT"]
            master_data["mood"] = random.randint(40, 80) # Simulated Market Mood
            master_data["logs"] = f"NSE Data Synced at {time.strftime('%H:%M:%S')}"
        except: 
            pass
        time.sleep(5)

@app.route("/api/data")
def get_data(): return jsonify(master_data)

@app.route("/api/status", methods=['POST'])
def status():
    global bot_active
    bot_active = request.json.get('active')
    return jsonify({"status": bot_active})

if __name__ == "__main__":
    threading.Thread(target=bharat_scanner_logic, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
