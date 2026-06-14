def check_signals(data):
    # Yahan apni strategy ka logic likho
    # Jaise: agar price 50,000 se kam hai toh BUY
    price = data['last']
    
    if price < 50000:
        return "BUY"
    return "HOLD"
