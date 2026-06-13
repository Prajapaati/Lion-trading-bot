from fastapi import FastAPI
import asyncio
import os

app = FastAPI()

# Bot ki current state check karne ke liye variable
BOT_STATUS = "STOPPED"

@app.get("/")
def home():
    return {"status": "Online", "bot_running_status": BOT_STATUS}

@app.get("/start")
def start_bot():
    global BOT_STATUS
    BOT_STATUS = "RUNNING"
    return {"message": "Bot successfully started"}

@app.get("/stop")
def stop_bot():
    global BOT_STATUS
    BOT_STATUS = "STOPPED"
    return {"message": "Bot successfully stopped"}

# --- 24/7 HEAVY STRATEGY LOOP ---
async def trading_loop():
    global BOT_STATUS
    while True:
        if BOT_STATUS == "RUNNING":
            print("Checking Strategy Rules...")
            # 1. Yahan market ka live data fetch hoga
            # 2. Aapke Heavy Rules check honge (e.g., Candlestick patterns, indicators)
            # 3. Agar rule match hua -> Trade execute hogi automatically
            
        await asyncio.sleep(2) # Har 2 second me run hoga (Adjustable)

@app.on_event("startup")
async def startup_event():
    # Jaise hi server on hoga, ye background loop apne aap chalu ho jayega
    asyncio.create_task(trading_loop())
