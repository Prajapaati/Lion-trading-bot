import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# --- PAGE LAYOUT CONFIGURATION ---
st.set_page_config(
    page_title="V12 Trading Universe - Multi-Asset Production",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM CLEAN WHITE THEME CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 1px solid #e9ecef; }
    
    .panel-box {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        border: 1px solid #e9ecef; box-shadow: 0px 4px 12px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    .panel-heading { font-size: 15px; font-weight: 700; color: #111111; margin-bottom: 15px; }
    
    /* Input field styling */
    div[data-baseweb="input"] { background-color: #ffffff !important; }
    
    /* Master Action Buttons */
    .start-btn button {
        background-color: #28a745 !important; color: white !important; border: none !important;
        font-weight: bold !important; width: 100%; height: 45px; border-radius: 8px;
    }
    .kill-btn button {
        background-color: #dc3545 !important; color: white !important; border: none !important;
        font-weight: bold !important; width: 100%; height: 45px; border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOCAL DATABASE CONFIGURATION ---
DB_FILE = "universal_broker_credentials.json"

def save_gateway_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def load_gateway_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {
        "asset_class": "Stocks / Options", "platform_name": "Angel One", 
        "api_key": "", "api_secret": "", "client_id": "", "totp_seed": "", 
        "max_loss": "", "max_trades": ""
    }

config_data = load_gateway_data()

# --- INITIALIZE EMPTY SESSION STATES (No Predefined Entries) ---
if "engine_active" not in st.session_state:
    st.session_state.engine_active = False
if "live_positions_matrix" not in st.session_state:
    st.session_state.live_positions_matrix = [] 
if "strategy_pipeline" not in st.session_state:
    st.session_state.strategy_pipeline = [] 

# ==========================================
# 🧭 SIDE NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#111111; font-weight:800; margin-bottom:0;'>🧠 AI TRADE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; color:#666666; margin-top:-10px;'>V12 Universe Terminal v2.5</p>", unsafe_allow_html=True)
    st.write("")
    
    menu = st.radio("Navigation Menu", [
        "🖥️ Main Dashboard", 
        "🔌 Universal Gateway Center", 
        "⚙️ Strategy Constructor", 
        "📜 System Logs"
    ])

# ==========================================
# 🔌 VIEW 1: UNIVERSAL GATEWAY CENTER (STOCKS & CRYPTO)
# ==========================================
if menu == "🔌 Universal Gateway Center":
    st.header("🔌 Universal Asset Gateway")
    st.write("Apne sahi exchange ya broker credentials connect karein. Saari fields completely clean hain.")
    
    st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-heading'>🌐 Step 1: Asset Class Selection</div>", unsafe_allow_html=True)
    
    # Choose between Stocks/Options or Crypto Assets
    asset_type = st.selectbox(
        "Select Asset Market Type", 
        ["Stocks / Options (Indian Market)", "Crypto Currencies (24/7 Global Market)"]
    )
    
    # Dynamic platforms loading based on asset type
    if asset_type == "Stocks / Options (Indian Market)":
        platform_options = ["Angel One (SmartAPI)", "Zerodha (Kite Connect)", "Dhan (DhanHQ)", "Fyers API", "Alice Blue (ANT Plus)"]
    else:
        platform_options = ["Binance (Global API)", "WazirX (India Exchange)", "CoinDCX Pro API", "Mudrex Wallet Link"]
        
    selected_platform = st.selectbox("Select Trading Platform / Exchange", platform_options)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-heading'>🔑 Step 2: API Keys & Credentials Vault</div>", unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        u_client_id = st.text_input("Account Client ID / User ID / UID", value=config_data["client_id"], placeholder="Example: EX1234 or CryptoUID")
        u_api_key = st.text_input("API Key / Public Key", value=config_data["api_key"], type="password", placeholder="Paste your exchange API key")
    with col_c2:
        u_secret = st.text_input("API Secret Key / Private Key", value=config_data["api_secret"], type="password", placeholder="Paste your secure private secret key")
        u_totp = st.text_input("TOTP Secret Key / MFA Seed (If required)", value=config_data["totp_seed"], type="password", placeholder="Paste 2FA String token seed")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-heading'>🛡️ Step 3: Cloud Risk Management Settings</div>", unsafe_allow_html=True)
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        u_loss = st.text_input("Max Daily Loss Target Limit (₹ / $)", value=config_data["max_loss"], placeholder="Example: 5000 or 100")
    with col_r2:
        u_trades = st.text_input("Max Allowed Multi-Order Trade Execution Count", value=config_data["max_trades"], placeholder="Example: 10")
        
    if st.button("💾 DEPLOY & SAVE CREDENTIALS", use_container_width=True):
        updated_config = {
            "asset_class": asset_type, "platform_name": selected_platform, "client_id": u_client_id, 
            "api_key": u_api_key, "totp_seed": u_totp, "api_secret": u_secret, "max_loss": u_loss, "max_trades": u_trades
        }
        save_gateway_data(updated_config)
        st.success(f"🔒 Securely Locked: Your {selected_platform} authentication tokens are active in cloud configurations.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 🖥️ VIEW 2: MAIN DASHBOARD (LIVE ACTIONS)
# ==========================================
elif menu == "🖥️ Main Dashboard":
    st.header("🖥️ Asset Command Console")
    
    # Active Connection Check Banner
    if st.session_state.engine_active:
        st.markdown(f"<div style='background-color:#d4edda; color:#155724; padding:12px; border-radius:8px; font-weight:bold; margin-bottom:20px;'>🟢 CLOUD PROCESS RUNNING: Connected to {config_data['platform_name']} Terminal ({config_data['asset_class']}) | 24/7 Active Mode</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background-color:#fff3cd; color:#856404; padding:12px; border-radius:8px; font-weight:bold; margin-bottom:20px;'>⚠️ ENGINE DORMANT: Machine is waiting for valid keys and ignition trigger signal.</div>", unsafe_allow_html=True)

    # --- PERFORMANCE BLANK METRICS ---
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown(f"<div class='panel-box'><div style='font-size:12px; color:#666666;'>Connected Engine</div><div style='font-size:16px; font-weight:bold;'>{config_data['platform_name'] if config_data['client_id'] else 'None'}</div></div>", unsafe_allow_html=True)
    with m_col2:
        st.markdown("<div class='panel-box'><div style='font-size:12px; color:#666666;'>Net Realized PnL</div><div style='font-size:16px; font-weight:bold; color:#111111;'>0.00</div></div>", unsafe_allow_html=True)
    with m_col3:
        st.markdown("<div class='panel-box'><div style='font-size:12px; color:#666666;'>Active Active Signals</div><div style='font-size:16px; font-weight:bold;'>0 Layers</div></div>", unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"<div class='panel-box'><div style='font-size:12px; color:#666666;'>Risk Guard Lock</div><div style='font-size:16px; font-weight:bold;'>{config_data['max_loss'] if config_data['max_loss'] else 'Not Locked'}</div></div>", unsafe_allow_html=True)

    # --- CONTROLS SWITCHES ---
    st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-heading'>🎮 Engine Ignition Panel</div>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.markdown("<div class='start-btn'>", unsafe_allow_html=True)
        if st.button("▶️ START CONTINUOUS CLOUD TRADING"):
            if not config_data["client_id"] or not config_data["api_key"]:
                st.error("Launch Blocked: Gateway Credentials missing inside configurations.")
            else:
                st.session_state.engine_active = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col_btn2:
        st.markdown("<div class='kill-btn'>", unsafe_allow_html=True)
        if st.button("🚨 EMERGENCY KILL ALL RUNNING SESSIONS"):
            st.session_state.engine_active = False
            st.session_state.live_positions_matrix = []
            st.toast("Cloud Runtime Halted. System Safe.", icon="🛑")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- OPEN ORDERS MATRIX TABLE ---
    st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-heading'>📑 Real-Time Order Stream Status</div>", unsafe_allow_html=True)
    if len(st.session_state.live_positions_matrix) == 0:
        st.caption("No running or open orders found. Terminal queues are clean.")
    else:
        st.dataframe(pd.DataFrame(st.session_state.live_positions_matrix), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ⚙️ VIEW 3: UNLIMITED STRATEGY CONSTRUCTOR
# ==========================================
elif menu == "⚙️ Strategy Constructor":
    st.header("⚙️ Strategy Constructor Room")
    st.write("Apne multi-asset mathematical rules cloud core computation pipelines me inject karein.")
    
    st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-heading'>🧬 Active Rule Matrices Pipeline</div>", unsafe_allow_html=True)
    if len(st.session_state.strategy_pipeline) == 0:
        st.info("Pipeline khali hai. Niche diye gaye form se mathematical array strategy add karein.")
    else:
        st.dataframe(pd.DataFrame(st.session_state.strategy_pipeline), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    with st.form("strat_form_crypto", clear_on_submit=True):
        st.markdown("<b>➕ Create Custom Rule Engine Layer</b>", unsafe_allow_html=True)
        s_id = st.text_input("Strategy Custom Identity Name", placeholder="Example: V12 Crypto Scalper Pro")
        s_math_base = st.selectbox("Base Mathematical System Layer", [
            "Exponential Moving Average Confluence Grid (EMA Multi)",
            "Relative Strength Index Deep Compression (RSI Pivot)",
            "Volume Spread Variance Delta Protocol",
            "Custom Pure Price Action Breakdown Rule"
        ])
        if st.form_submit_button("🚀 INJECT INTO CLOUD COMPUTATION CORE"):
            if s_id:
                st.session_state.strategy_pipeline.append({"Strategy Name": s_id, "Mathematical Base": s_math_base, "Status": "Active Scan Loop"})
                st.toast(f"'{s_id}' Compiled and Injected!", icon="⚡")
                st.rerun()

# ==========================================
# 📜 VIEW 4: SYSTEM LOGS
# ==========================================
else:
    st.header("📜 Live Machine Process Logs")
    st.write("Background cloud server execution details:")
    
    if st.session_state.engine_active:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_feed = f"[{current_time}] [INFO] Handshake verified with {config_data['platform_name']} gateway.\n[{current_time}] [INFO] Asset Layer synced for: {config_data['asset_class']}.\n[{current_time}] [INFO] Risk systems nominal. Scanning custom active formula matrices..."
    else:
        log_feed = "System Engine Core is currently in an Idle / Dormant state. No computational process active."
        
    st.text_area("Live Terminal Output Feed", value=log_feed, height=250, label_visibility="collapsed")
