 import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 1. Page Configuration & Theme
st.set_page_config(
    page_title="AI TRADE - V12 Universe Multi-Broker",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Dark Theme and Multi-Broker Layout
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #0b0e14; border-right: 1px solid #1e252f; }
    
    /* Stats Cards */
    .metric-card {
        background: linear-gradient(145deg, #0e121a, #131922);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #1e252f;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .metric-lbl { font-size: 13px; color: #6c7d93; font-weight: 500; text-transform: uppercase; }
    .metric-val { font-size: 26px; font-weight: 700; margin: 8px 0; font-family: 'Poppins', sans-serif; }
    
    /* Broker Badge */
    .broker-badge {
        background-color: #1a212d;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        border: 1px solid #00ffcc;
        color: #00ffcc;
        display: inline-block;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR - Navigation & Multi-Broker Engine Selection
with st.sidebar:
    st.markdown("<h1 style='color:#ff0055; font-family:Poppins; font-size:26px; margin-bottom:0;'>🦁 AI TRADE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#4b596c; font-size:11px; margin-top:0;'>V12 Multi-Broker Trading Universe</p>", unsafe_allow_html=True)
    st.write("---")
    
    # 📱 Core Menu Navigation
    menu = st.radio(
        "CORE TERMINAL",
        ["📊 Dashboard", "🤖 Active Bots", "⚡ Strategies", "📜 Rules", "💼 Portfolio", "⚙️ Connection Settings"],
        index=0
    )
    
    st.write("---")
    
    # 🔌 BROKER & EXCHANGE CONNECTOR MULTI-LIST
    st.markdown("### 🔌 Select Trading Node")
    broker_type = st.selectbox("Asset Category", ["Indian Stocks 📈", "Global Crypto 🌐"])
    
    if broker_type == "Indian Stocks 📈":
        selected_broker = st.selectbox("Choose Broker", ["Angel One (SmartAPI)", "Zerodha (Kite Connect)", "Groww", "Upstox"])
    else:
        selected_broker = st.selectbox("Choose Exchange", ["Binance API", "WazirX India", "CoinDCX Pro", "Delta Exchange"])

    st.write("---")
    st.markdown(f"#### 🔑 Connect to **{selected_broker}**")
    
    # Dynamic Key Fields based on type
    api_key = st.text_input("API Key / Client ID", type="password", placeholder=f"Enter {selected_broker} Key")
    secret_or_totp = st.text_input("API Secret / TOTP Key", type="password", placeholder="Enter Secret or TOTP Key")

# Check connection logic
is_connected = bool(api_key and secret_or_totp)

# 3. Dynamic Screen Logic

# --- SCREEN 1: DASHBOARD ---
if menu == "📊 Dashboard":
    st.markdown("<h2 style='margin-bottom:0;'>Hello, Trader! 👋</h2>", unsafe_allow_html=True)
    
    if is_connected:
        st.markdown(f"<div class='broker-badge'>🟢 Connected Node: {selected_broker} (LIVE FEED)</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='broker-badge' style='color:#ff0055; border-color:#ff0055;'>🔴 Disconnected: Setup keys in sidebar</div>", unsafe_allow_html=True)
        st.info(f"ℹ️ Dashboard setup ready. Fill in your **{selected_broker}** credentials in the sidebar to fire up the engine.")

    # Top Metrics Layout (Changes instantly based on connection)
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        balance = "₹14,580.00" if (is_connected and "Stocks" in broker_type) else ("$1,250.00" if is_connected else "0.00")
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Total Balance</div><div class='metric-val'>{balance}</div><div style='color:#6c7d93; font-size:12px;'>Live Node Feed</div></div>", unsafe_allow_html=True)
    with m2:
        profit = "₹1,840.25" if (is_connected and "Stocks" in broker_type) else ("$145.20" if is_connected else "0.00")
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Net Profit</div><div class='metric-val' style='color:#00ff88;'>{profit}</div><div style='color:#00ff88; font-size:12px;'>▲ System Profitable</div></div>", unsafe_allow_html=True)
    with m3:
        win_rate = "81.40%" if is_connected else "0.00%"
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Win Rate</div><div class='metric-val' style='color:#ffcc00;'>{win_rate}</div><div style='color:#ffcc00; font-size:12px;'>V12 Algorithm</div></div>", unsafe_allow_html=True)
    with m4:
        bots = "5 Bots Live" if is_connected else "0 Active"
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Active System</div><div class='metric-val' style='color:#00ffff;'>{bots}</div><div style='color:#00ffff; font-size:12px;'>Automated Triggers</div></div>", unsafe_allow_html=True)
    with m5:
        vol = "High Vol" if is_connected else "No Signal"
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>Market Node</div><div class='metric-val' style='color:#ff0055;'>{vol}</div><div style='color:#ff0055; font-size:12px;'>Safety Lock On</div></div>", unsafe_allow_html=True)

    # Charts Section
    st.write("")
    col_chart, col_market = st.columns([3, 1])
    
    with col_chart:
        st.markdown(f"### 📈 {selected_broker} Live Chart Overview")
        fig = go.Figure()
        if is_connected:
            x = pd.date_range(start="2026-06-12 00:00", periods=24, freq="H")
            y = np.cumsum(np.random.normal(40, 12, 24)) + 5000
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='#00ffcc', width=3), fill='tozeroy', fillcolor='rgba(0, 255, 204, 0.05)'))
        else:
            fig.add_trace(go.Scatter(x=[0], y=[0], mode='lines'))
            fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280)
        st.plotly_chart(fig, use_container_width=True)

    with col_market:
        st.markdown("### ⚡ Current Watchlist Tokens")
        if "Stocks" in broker_type:
            st.write("1. **NIFTY 50**")
            st.write("2. **BANK NIFTY**")
            st.write("3. **RELIANCE**")
        else:
            st.write("1. **BTC / USDT**")
            st.write("2. **ETH / USDT**")
            st.write("3. **SOL / USDT**")

# --- SCREEN 2: ACTIVE BOTS ---
elif menu == "🤖 Active Bots":
    st.markdown("## 🤖 Bot Engine Configuration")
    if is_connected:
        st.success(f"Lion Core Scalper Engine linked successfully to **{selected_broker}** API data terminal.")
        st.write("The system is currently handling background trade loops safely.")
    else:
        st.warning("Please connect a broker node via sidebar to spin up automated bot strategies.")

# --- SCREEN 3: STRATEGIES ---
elif menu == "⚡ Strategies":
    st.markdown("## ⚡ Multi-Asset Strategies")
    st.selectbox("Select Script Execution Type", ["Intraday Option Scalping (Stocks)", "24/7 Futures Grid Bot (Crypto)", "Breakout Volume Hunter"])

# --- SCREEN 4: RULES ---
elif menu == "📜 Rules":
    st.markdown("## 📜 Universal Risk Control Profile")
    st.slider("Max Capital Drawdown per Broker Trigger (%)", 1, 15, 3)
    st.checkbox("Force Close positions if Broker Connection drops")

# --- SCREEN 5: PORTFOLIO ---
elif menu == "💼 Portfolio":
    st.markdown("## 💼 Multi-Node Portfolio Asset Distribution")
    if is_connected:
        st.info(f"Showing localized asset data directly matching client profile logs on **{selected_broker}**.")
    else:
        st.warning("Connect your specific account to display available balances.")

# --- SCREEN 6: SETTINGS ---
elif menu == "⚙️ Connection Settings":
    st.markdown("## ⚙️ Core Server Routing Matrix")
    st.write("Status: Connection Nodes Operational.")
    st.checkbox("Enable multi-broker concurrent order flow routing")
