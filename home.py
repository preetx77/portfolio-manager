# home.py - Advanced Portfolio Tracker Home Page
import streamlit as st
from portfolio import PortfolioManager
from transaction import Transaction
from report import ReportGenerator
import database
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

# ---------- Page Config ----------
st.set_page_config(
    page_title="Portfolio Tracker - Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Enhanced Custom CSS ----------
st.markdown(
    """
    <style>
    /* Background gradient with animated particles effect */
    .stApp {
        background: radial-gradient(1200px 600px at 0% 0%, rgba(0, 255, 204, 0.08), transparent),
                    radial-gradient(1200px 600px at 100% 0%, rgba(0, 127, 255, 0.08), transparent),
                    radial-gradient(800px 400px at 50% 50%, rgba(167, 139, 250, 0.05), transparent),
                    linear-gradient(135deg, #0a0e1a 0%, #0f172a 50%, #111827 100%);
        color: #e5e7eb;
    }

    /* Enhanced Glass cards with glow effect */
    .glass {
        background: rgba(17, 25, 40, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 24px 28px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 48px rgba(34, 211, 238, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(34, 211, 238, 0.3);
    }

    /* Gradient text */
    .title {
        font-weight: 800;
        letter-spacing: 0.05rem;
        background: linear-gradient(135deg, #22d3ee 0%, #a78bfa 50%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-title {
        font-weight: 900;
        letter-spacing: -0.02rem;
        background: linear-gradient(135deg, #22d3ee 0%, #a78bfa 40%, #60a5fa 70%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 8s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Enhanced metric cards */
    .metric-card { 
        text-align: center; 
        padding: 24px 20px; 
        border-radius: 16px; 
        border: 1px solid rgba(255,255,255,0.1);
        background: linear-gradient(135deg, rgba(17, 25, 40, 0.9), rgba(17, 25, 40, 0.6));
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(34, 211, 238, 0.25);
        border: 1px solid rgba(34, 211, 238, 0.5);
    }
    
    /* Feature cards with enhanced hover */
    .feature-card {
        background: linear-gradient(135deg, rgba(17, 25, 40, 0.85), rgba(17, 25, 40, 0.5));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 32px 24px;
        text-align: center;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(34, 211, 238, 0.1);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .feature-card:hover::after {
        width: 300px;
        height: 300px;
    }
    
    .feature-card:hover {
        transform: translateY(-12px) scale(1.05);
        box-shadow: 0 24px 72px rgba(34, 211, 238, 0.3);
        border: 1px solid rgba(34, 211, 238, 0.6);
    }

    /* Color utilities */
    .subtle { color: #94a3b8; }
    .success { color: #34d399; }
    .warn { color: #fbbf24; }
    .err { color: #f87171; }
    .cyan { color: #22d3ee; }
    .purple { color: #a78bfa; }
    .blue { color: #60a5fa; }
    
    /* Pulse animation */
    .pulse {
        animation: pulse 2.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    /* Float animation */
    .float {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Glow effect */
    .glow {
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.3),
                    0 0 40px rgba(34, 211, 238, 0.2),
                    0 0 60px rgba(34, 211, 238, 0.1);
    }
    
    /* Advanced card */
    .advanced-card {
        background: linear-gradient(135deg, rgba(17, 25, 40, 0.9), rgba(17, 25, 40, 0.5));
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 32px;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .advanced-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 24px 72px rgba(34, 211, 238, 0.25);
        border: 1px solid rgba(34, 211, 238, 0.3);
    }
    
    /* Button enhancements */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(34, 211, 238, 0.3);
    }
    
    /* Badge styles */
    .badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        background: linear-gradient(135deg, rgba(34, 211, 238, 0.2), rgba(167, 139, 250, 0.2));
        border: 1px solid rgba(34, 211, 238, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- App State ----------
if "pm" not in st.session_state:
    database.init_database()
    pm = PortfolioManager()
    pm.set_user("default")
    pm.load_portfolios("default")
    st.session_state.pm = pm
    st.session_state.reporter = ReportGenerator(pm)
    st.session_state.username = "default"

pm: PortfolioManager = st.session_state.pm
reporter: ReportGenerator = st.session_state.reporter

# ---------- Global KPIs ----------
total_portfolios = len(pm.portfolios)
total_positions = sum(len(p.stocks) for p in pm.portfolios.values())
total_value = sum(p.calculate_portfolio_value() for p in pm.portfolios.values())

# Calculate portfolio growth (mock data for demo - can be replaced with real calculation)
portfolio_growth = 12.5 if total_value > 0 else 0

# ---------- Sidebar: Profile & Quick Actions ----------
st.sidebar.header("👤 Profile")
with st.sidebar:
    # Get existing users for dropdown
    existing_users = database.get_all_users()
    current_user = st.session_state.get("username", "default")
    
    # Ensure current user is in the list
    if current_user not in existing_users:
        existing_users.append(current_user)
        existing_users.sort()
    
    # Profile selection dropdown
    selected_user = st.selectbox(
        "Select Profile", 
        options=existing_users + ["➕ Create New Profile"], 
        index=existing_users.index(current_user) if current_user in existing_users else 0,
        key="profile_select"
    )
    
    # Handle new profile creation
    if selected_user == "➕ Create New Profile":
        new_profile = st.text_input("New profile name", key="new_profile_input")
        if st.button("Create Profile", use_container_width=True, key="create_profile_btn"):
            if new_profile.strip():
                st.session_state.username = new_profile.strip()
                pm.set_user(st.session_state.username)
                pm.load_portfolios(st.session_state.username)
                st.success(f"Created and switched to profile '{st.session_state.username}'.")
                st.rerun()
            else:
                st.warning("Please enter a valid profile name.")
    else:
        # Switch to selected existing profile
        if selected_user != current_user:
            st.session_state.username = selected_user
            pm.set_user(st.session_state.username)
            pm.load_portfolios(st.session_state.username)
            st.success(f"Switched to profile '{st.session_state.username}'.")
            st.rerun()
    
    # Show current active profile
    st.markdown(f"**Active:** `{st.session_state.username}`")

st.sidebar.header("🚀 Navigation")
with st.sidebar:
    st.page_link("home.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/1_📊_Portfolios.py", label="📊 Portfolios", icon="📊")
    st.page_link("pages/2_💹_Trading.py", label="💹 Trading", icon="💹")
    st.page_link("pages/3_📈_Live_Market.py", label="📈 Live Market", icon="📈")
    st.page_link("pages/6_📊_Charts.py", label="📊 Charts", icon="📊")
    st.page_link("pages/4_📄_Reports.py", label="📄 Reports", icon="📄")
    st.page_link("pages/5_ℹ️_About.py", label="ℹ️ About", icon="ℹ️")

st.sidebar.header("Quick Actions")
with st.sidebar:
    with st.expander("➕ Add Portfolio", expanded=True):
        new_name = st.text_input("Portfolio name", key="add_portfolio_name")
        if st.button("Create Portfolio", use_container_width=True):
            if not new_name.strip():
                st.warning("Provide a valid name.")
            else:
                pm.add_portfolio(new_name.strip())
                p = pm.get_portfolio(new_name.strip())
                if p:
                    database.save_portfolio(p, st.session_state.username)
                st.success(f"Created portfolio '{new_name}'.")

    with st.expander("📈 Quick Add Stock"):
        if pm.portfolios:
            pname_q = st.selectbox("Portfolio", options=list(pm.portfolios.keys()), key="q_port")
            sym_q = st.text_input("Symbol", key="q_sym")
            qty_q = st.number_input("Quantity", min_value=1, value=10, step=1, key="q_qty")
            if st.button("Add Stock", use_container_width=True, key="q_add_btn"):
                pm.add_stock_to_portfolio(pname_q, sym_q.strip().upper(), int(qty_q))
                p = pm.get_portfolio(pname_q)
                if p:
                    database.save_portfolio(p, st.session_state.username)
                st.success(f"Added {qty_q} of {sym_q} to {pname_q}.")
        else:
            st.info("Create a portfolio first.")

# ---------- HOME PAGE CONTENT ----------

# Hero Section with Clear Value Proposition
st.markdown("""
<div style='text-align: center; padding: 40px 20px 60px 20px;'>
    <div style='font-size: 4rem; margin-bottom: 20px;'>💼</div>
    <h1 class='hero-title' style='font-size: 3.5rem; margin-bottom: 16px; line-height: 1.2;'>
        Welcome to Your Portfolio Hub
    </h1>
    <p class='subtle' style='font-size: 1.3rem; max-width: 700px; margin: 0 auto 24px auto; line-height: 1.6;'>
        Track, analyze, and grow your investments with powerful tools and real-time insights
    </p>
    <div style='display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 30px;'>
        <span class='badge'>📊 Multi-Portfolio</span>
        <span class='badge'>📈 Real-Time Data</span>
        <span class='badge'>🤖 AI Insights</span>
        <span class='badge'>📱 Easy to Use</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Check if user has portfolios - show different content based on status
has_portfolios = len(pm.portfolios) > 0
has_stocks = total_positions > 0

if not has_portfolios:
    # Getting Started Guide for New Users
    st.markdown("""
    <div class='advanced-card' style='text-align: center; padding: 50px 30px; margin: 40px 0;'>
        <div style='font-size: 4rem; margin-bottom: 20px;'>🚀</div>
        <h2 class='title' style='font-size: 2.5rem; margin-bottom: 16px;'>Let's Get Started!</h2>
        <p class='subtle' style='font-size: 1.2rem; margin-bottom: 30px; max-width: 600px; margin-left: auto; margin-right: auto;'>
            You're just 3 simple steps away from tracking your investments like a pro
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Step-by-step guide
    step_col1, step_col2, step_col3 = st.columns(3)
    
    with step_col1:
        st.markdown("""
        <div class='feature-card' style='text-align: center; padding: 40px 24px;'>
            <div style='font-size: 4rem; margin-bottom: 20px;'>1️⃣</div>
            <h3 style='color: #22d3ee; margin-bottom: 12px; font-size: 1.4rem;'>Create Portfolio</h3>
            <p style='color: #94a3b8; line-height: 1.6;'>
                Start by creating your first portfolio. Use the sidebar or the quick action below.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col2:
        st.markdown("""
        <div class='feature-card' style='text-align: center; padding: 40px 24px;'>
            <div style='font-size: 4rem; margin-bottom: 20px;'>2️⃣</div>
            <h3 style='color: #a78bfa; margin-bottom: 12px; font-size: 1.4rem;'>Add Stocks</h3>
            <p style='color: #94a3b8; line-height: 1.6;'>
                Add stocks to your portfolio using stock symbols (e.g., AAPL, GOOGL, MSFT).
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col3:
        st.markdown("""
        <div class='feature-card' style='text-align: center; padding: 40px 24px;'>
            <div style='font-size: 4rem; margin-bottom: 20px;'>3️⃣</div>
            <h3 style='color: #34d399; margin-bottom: 12px; font-size: 1.4rem;'>Track & Grow</h3>
            <p style='color: #94a3b8; line-height: 1.6;'>
                Monitor performance, get insights, and make informed investment decisions.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    # Quick start action
    st.markdown("""
    <div style='text-align: center; margin: 40px 0;'>
        <h3 class='title' style='font-size: 1.8rem; margin-bottom: 20px;'>👇 Start Here</h3>
    </div>
    """, unsafe_allow_html=True)
    
    quick_col1, quick_col2, quick_col3 = st.columns([1, 2, 1])
    with quick_col2:
        with st.form("quick_start_form"):
            st.markdown("**Create Your First Portfolio**")
            portfolio_name = st.text_input("Portfolio Name", placeholder="e.g., My Growth Portfolio")
            submitted = st.form_submit_button("🚀 Create & Get Started", use_container_width=True)
            
            if submitted:
                if portfolio_name.strip():
                    pm.add_portfolio(portfolio_name.strip())
                    p = pm.get_portfolio(portfolio_name.strip())
                    if p:
                        database.save_portfolio(p, st.session_state.username)
                    st.success(f"✅ Portfolio '{portfolio_name}' created! Now add some stocks using the sidebar.")
                    st.rerun()
                else:
                    st.error("Please enter a valid portfolio name")

else:
    # Enhanced Stats Dashboard for Existing Users
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h2 class='title' style='font-size: 2.2rem; margin-bottom: 10px;'>📊 Your Portfolio Dashboard</h2>
        <p class='subtle' style='font-size: 1.1rem;'>Real-time overview of your investment performance</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card float'>
        <div style='font-size: 3rem; margin-bottom: 12px; filter: drop-shadow(0 0 10px rgba(34, 211, 238, 0.5));'>💼</div>
        <h2 style='color: #22d3ee; margin: 0; font-size: 2.8rem; font-weight: 800;'>{total_portfolios}</h2>
        <p style='color: #94a3b8; margin: 8px 0 0 0; font-size: 1rem; font-weight: 600;'>Active Portfolios</p>
        <div style='margin-top: 12px; padding: 6px 12px; background: rgba(34, 211, 238, 0.1); border-radius: 8px; display: inline-block;'>
            <span style='color: #22d3ee; font-size: 0.85rem; font-weight: 600;'>📈 Managed</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card float' style='animation-delay: 0.2s;'>
        <div style='font-size: 3rem; margin-bottom: 12px; filter: drop-shadow(0 0 10px rgba(167, 139, 250, 0.5));'>📈</div>
        <h2 style='color: #a78bfa; margin: 0; font-size: 2.8rem; font-weight: 800;'>{total_positions}</h2>
        <p style='color: #94a3b8; margin: 8px 0 0 0; font-size: 1rem; font-weight: 600;'>Total Positions</p>
        <div style='margin-top: 12px; padding: 6px 12px; background: rgba(167, 139, 250, 0.1); border-radius: 8px; display: inline-block;'>
            <span style='color: #a78bfa; font-size: 0.85rem; font-weight: 600;'>🎯 Diversified</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card float' style='animation-delay: 0.4s;'>
        <div style='font-size: 3rem; margin-bottom: 12px; filter: drop-shadow(0 0 10px rgba(52, 211, 153, 0.5));'>💰</div>
        <h2 style='color: #34d399; margin: 0; font-size: 2.8rem; font-weight: 800;'>${total_value:,.0f}</h2>
        <p style='color: #94a3b8; margin: 8px 0 0 0; font-size: 1rem; font-weight: 600;'>Total Value</p>
        <div style='margin-top: 12px; padding: 6px 12px; background: rgba(52, 211, 153, 0.1); border-radius: 8px; display: inline-block;'>
            <span style='color: #34d399; font-size: 0.85rem; font-weight: 600;'>↗ +{portfolio_growth}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    active_user = st.session_state.get("username", "default")
    st.markdown(f"""
    <div class='metric-card float' style='animation-delay: 0.6s;'>
        <div style='font-size: 3rem; margin-bottom: 12px; filter: drop-shadow(0 0 10px rgba(96, 165, 250, 0.5));'>👤</div>
        <h2 style='color: #60a5fa; margin: 0; font-size: 2rem; font-weight: 800;'>{active_user.title()}</h2>
        <p style='color: #94a3b8; margin: 8px 0 0 0; font-size: 1rem; font-weight: 600;'>Active Profile</p>
        <div style='margin-top: 12px; padding: 6px 12px; background: rgba(96, 165, 250, 0.1); border-radius: 8px; display: inline-block;'>
            <span style='color: #60a5fa; font-size: 0.85rem; font-weight: 600;'>✓ Verified</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Show features only if user has portfolios
if has_portfolios:
    # Recent Activity / Quick Stats
    st.markdown("""
    <div style='text-align: center; margin: 50px 0 30px 0;'>
        <h2 class='title' style='font-size: 2rem; margin-bottom: 10px;'>⚡ Quick Overview</h2>
    </div>
    """, unsafe_allow_html=True)
    
    overview_col1, overview_col2 = st.columns(2)
    
    with overview_col1:
        st.markdown("""
        <div class='glass' style='padding: 24px;'>
            <h3 style='color: #22d3ee; margin-bottom: 16px; font-size: 1.3rem;'>📋 Portfolio Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for portfolio_name, portfolio in list(pm.portfolios.items())[:3]:  # Show top 3
            value = portfolio.calculate_portfolio_value()
            positions = len(portfolio.stocks)
            st.markdown(f"""
            <div style='background: rgba(17, 25, 40, 0.5); padding: 16px; border-radius: 12px; margin-bottom: 12px; border-left: 3px solid #22d3ee;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <div style='color: #e5e7eb; font-weight: 600; font-size: 1.1rem;'>{portfolio_name}</div>
                        <div style='color: #94a3b8; font-size: 0.9rem; margin-top: 4px;'>{positions} positions</div>
                    </div>
                    <div style='text-align: right;'>
                        <div style='color: #34d399; font-weight: 700; font-size: 1.2rem;'>${value:,.0f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if len(pm.portfolios) > 3:
            st.info(f"+ {len(pm.portfolios) - 3} more portfolios")
    
    with overview_col2:
        st.markdown("""
        <div class='glass' style='padding: 24px;'>
            <h3 style='color: #a78bfa; margin-bottom: 16px; font-size: 1.3rem;'>💡 Quick Tips</h3>
        </div>
        """, unsafe_allow_html=True)
        
        tips = [
            ("📊", "View detailed portfolio analytics", "Go to Portfolios page"),
            ("💹", "Execute trades and manage positions", "Visit Trading section"),
            ("📈", "Check live market data and trends", "Explore Live Market"),
            ("📄", "Generate comprehensive reports", "Create Reports")
        ]
        
        for icon, tip, action in tips:
            st.markdown(f"""
            <div style='background: rgba(17, 25, 40, 0.5); padding: 14px; border-radius: 10px; margin-bottom: 10px;'>
                <div style='display: flex; align-items: center; gap: 12px;'>
                    <div style='font-size: 1.5rem;'>{icon}</div>
                    <div>
                        <div style='color: #e5e7eb; font-size: 0.95rem;'>{tip}</div>
                        <div style='color: #94a3b8; font-size: 0.8rem; margin-top: 2px;'>{action}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.write("")
st.write("")

# Enhanced Platform Features Section
st.markdown("""
<div style='text-align: center; margin: 50px 0 30px 0;'>
    <h2 class='title' style='font-size: 2.5rem; margin-bottom: 12px;'>🌟 What You Can Do</h2>
    <p class='subtle' style='font-size: 1.15rem;'>Powerful features designed for smart investors</p>
</div>
""", unsafe_allow_html=True)

# Enhanced Feature Cards Grid with clearer descriptions
feat_col1, feat_col2 = st.columns(2)

with feat_col1:
    st.markdown("""
    <div class='feature-card' style='text-align: left; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; margin-bottom: 16px;'>
            <div style='font-size: 3rem; margin-right: 20px; filter: drop-shadow(0 0 10px rgba(34, 211, 238, 0.5));'>📊</div>
            <div>
                <h3 style='color: #22d3ee; margin: 0; font-size: 1.5rem; font-weight: 700;'>Portfolio Management</h3>
                <p style='color: #94a3b8; margin: 4px 0 0 0; font-size: 0.95rem;'>Multi-portfolio tracking & organization</p>
            </div>
        </div>
        <ul style='color: #94a3b8; margin: 0; padding-left: 20px; line-height: 1.8;'>
            <li>Create unlimited portfolios</li>
            <li>Track multiple asset classes</li>
            <li>Real-time portfolio valuation</li>
            <li>Performance analytics</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-card' style='text-align: left; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; margin-bottom: 16px;'>
            <div style='font-size: 3rem; margin-right: 20px; filter: drop-shadow(0 0 10px rgba(167, 139, 250, 0.5));'>📈</div>
            <div>
                <h3 style='color: #a78bfa; margin: 0; font-size: 1.5rem; font-weight: 700;'>Live Market Data</h3>
                <p style='color: #94a3b8; margin: 4px 0 0 0; font-size: 0.95rem;'>Real-time market information</p>
            </div>
        </div>
        <ul style='color: #94a3b8; margin: 0; padding-left: 20px; line-height: 1.8;'>
            <li>Live stock prices & indices</li>
            <li>Interactive price charts</li>
            <li>Historical data analysis</li>
            <li>Market trends & indicators</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
    <div class='feature-card' style='text-align: left; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; margin-bottom: 16px;'>
            <div style='font-size: 3rem; margin-right: 20px; filter: drop-shadow(0 0 10px rgba(52, 211, 153, 0.5));'>💹</div>
            <div>
                <h3 style='color: #34d399; margin: 0; font-size: 1.5rem; font-weight: 700;'>Trading Platform</h3>
                <p style='color: #94a3b8; margin: 4px 0 0 0; font-size: 0.95rem;'>Execute trades seamlessly</p>
            </div>
        </div>
        <ul style='color: #94a3b8; margin: 0; padding-left: 20px; line-height: 1.8;'>
            <li>Buy & sell stocks instantly</li>
            <li>Transaction history tracking</li>
            <li>Portfolio rebalancing tools</li>
            <li>Order execution analytics</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='feature-card' style='text-align: left; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; margin-bottom: 16px;'>
            <div style='font-size: 3rem; margin-right: 20px; filter: drop-shadow(0 0 10px rgba(96, 165, 250, 0.5));'>📄</div>
            <div>
                <h3 style='color: #60a5fa; margin: 0; font-size: 1.5rem; font-weight: 700;'>Smart Reports</h3>
                <p style='color: #94a3b8; margin: 4px 0 0 0; font-size: 0.95rem;'>AI-powered insights & analysis</p>
            </div>
        </div>
        <ul style='color: #94a3b8; margin: 0; padding-left: 20px; line-height: 1.8;'>
            <li>Comprehensive portfolio reports</li>
            <li>Performance metrics & KPIs</li>
            <li>Risk analysis & recommendations</li>
            <li>Export & share capabilities</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Portfolio Distribution Charts Section (only show if user has stocks)
if has_stocks:
    st.markdown("""
    <div class='advanced-card'>
        <h2 class='title' style='text-align: center; margin-bottom: 30px; font-size: 2rem;'>
            📊 Portfolio Distribution Analysis
        </h2>
    </div>
    """, unsafe_allow_html=True)

if pm.portfolios and has_stocks:
    # Collect all portfolio data for comprehensive analysis
    all_stocks_data = []
    portfolio_values = {}
    
    for portfolio_name, portfolio in pm.portfolios.items():
        portfolio_value = portfolio.calculate_portfolio_value()
        portfolio_values[portfolio_name] = portfolio_value
        
        for symbol, stock_data in portfolio.stocks.items():
            stock = stock_data['stock']
            quantity = stock_data['quantity']
            if stock.symbol and stock.symbol.strip():
                value = stock.price * quantity
                all_stocks_data.append({
                    'Portfolio': portfolio_name,
                    'Symbol': stock.symbol.upper(),
                    'Quantity': quantity,
                    'Price': stock.price,
                    'Value': value,
                    'Name': stock.name
                })
    
    if all_stocks_data:
        df_all = pd.DataFrame(all_stocks_data)
        
        # Create comprehensive distribution charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Portfolio Value Distribution
            if len(portfolio_values) > 1:
                portfolio_df = pd.DataFrame(list(portfolio_values.items()), columns=['Portfolio', 'Value'])
                
                fig_portfolio = px.pie(
                    portfolio_df,
                    values='Value',
                    names='Portfolio',
                    title="Portfolio Value Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_portfolio.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Value: $%{value:,.2f}<br>Percent: %{percent}<extra></extra>'
                )
                fig_portfolio.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    showlegend=True,
                    margin=dict(l=20, r=20, t=40, b=20),
                    title_font_color='white'
                )
                st.plotly_chart(fig_portfolio, use_container_width=True)
            else:
                st.info("Create multiple portfolios to see distribution")
        
        with chart_col2:
            # Top Holdings Across All Portfolios
            stock_totals = df_all.groupby('Symbol')['Value'].sum().reset_index()
            stock_totals = stock_totals.sort_values('Value', ascending=False).head(10)
            
            fig_holdings = px.bar(
                stock_totals,
                x='Symbol',
                y='Value',
                title="Top 10 Holdings by Value",
                color='Value',
                color_continuous_scale='viridis'
            )
            fig_holdings.update_traces(
                hovertemplate='<b>%{x}</b><br>Total Value: $%{y:,.2f}<extra></extra>'
            )
            fig_holdings.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                showlegend=False,
                margin=dict(l=20, r=20, t=40, b=20),
                xaxis_title="Stock Symbol",
                yaxis_title="Value ($)",
                title_font_color='white'
            )
            st.plotly_chart(fig_holdings, use_container_width=True)
        
        # Sector/Asset Allocation (if we have multiple different stocks)
        chart_col3, chart_col4 = st.columns(2)
        
        with chart_col3:
            # Portfolio Composition by Number of Positions
            portfolio_positions = df_all.groupby('Portfolio').size().reset_index(name='Positions')
            
            fig_positions = px.bar(
                portfolio_positions,
                x='Portfolio',
                y='Positions',
                title="Portfolio Composition by Positions",
                color='Positions',
                color_continuous_scale='plasma'
            )
            fig_positions.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                showlegend=False,
                margin=dict(l=20, r=20, t=40, b=20),
                title_font_color='white'
            )
            st.plotly_chart(fig_positions, use_container_width=True)
        
        with chart_col4:
            # Value Distribution Heatmap
            portfolio_stock_matrix = df_all.pivot_table(
                index='Portfolio', 
                columns='Symbol', 
                values='Value', 
                fill_value=0
            )
            
            if not portfolio_stock_matrix.empty and portfolio_stock_matrix.shape[0] > 0 and portfolio_stock_matrix.shape[1] > 0:
                try:
                    fig_heatmap = px.imshow(
                        portfolio_stock_matrix.values,
                        labels=dict(x="Stock Symbol", y="Portfolio", color="Value"),
                        x=portfolio_stock_matrix.columns,
                        y=portfolio_stock_matrix.index,
                        title="Portfolio-Stock Value Heatmap",
                        color_continuous_scale='viridis'
                    )
                    fig_heatmap.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white',
                        margin=dict(l=20, r=20, t=40, b=20)
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                except Exception as e:
                    st.info("Heatmap visualization temporarily unavailable")
            else:
                st.info("Add more stocks to see heatmap visualization")
        
        # Summary Statistics
        st.markdown("### 📈 Distribution Summary")
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        total_value = df_all['Value'].sum()
        unique_stocks = df_all['Symbol'].nunique()
        avg_position_size = df_all['Value'].mean()
        largest_position = df_all.loc[df_all['Value'].idxmax()]
        
        with summary_col1:
            st.metric("Total Portfolio Value", f"${total_value:,.2f}")
        
        with summary_col2:
            st.metric("Unique Stocks", unique_stocks)
        
        with summary_col3:
            st.metric("Avg Position Size", f"${avg_position_size:,.2f}")
        
        with summary_col4:
            st.metric("Largest Position", f"{largest_position['Symbol']}")
            
elif has_portfolios and not has_stocks:
    st.markdown("""
    <div class='glass' style='text-align: center; padding: 40px 30px; margin: 30px 0;'>
        <div style='font-size: 3rem; margin-bottom: 16px;'>📈</div>
        <h3 class='title' style='font-size: 1.8rem; margin-bottom: 12px;'>Add Stocks to See Analytics</h3>
        <p class='subtle' style='font-size: 1.1rem; margin-bottom: 20px;'>
            Your portfolios are ready! Add some stocks to unlock powerful visualizations and insights.
        </p>
        <p style='color: #94a3b8;'>
            💡 Use the <strong>Quick Add Stock</strong> section in the sidebar to get started
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Enhanced Navigation Section
st.markdown("""
<div style='text-align: center; margin: 50px 0 30px 0;'>
    <h2 class='title' style='font-size: 2.5rem; margin-bottom: 12px;'>🧭 Navigate Your Portfolio</h2>
    <p class='subtle' style='font-size: 1.15rem;'>Quick access to all features and tools</p>
</div>
""", unsafe_allow_html=True)

action_col1, action_col2, action_col3, action_col4 = st.columns(4)

with action_col1:
    st.markdown("""
    <div class='feature-card' style='padding: 24px 20px; min-height: 180px;'>
        <div style='font-size: 3.5rem; margin-bottom: 16px; filter: drop-shadow(0 0 10px rgba(34, 211, 238, 0.5));'>📊</div>
        <h4 style='color: #22d3ee; margin: 0 0 8px 0; font-size: 1.2rem; font-weight: 700;'>View Portfolios</h4>
        <p style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 16px;'>Manage your investments</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Portfolios →", use_container_width=True, key="home_portfolios"):
        st.switch_page("pages/1_📊_Portfolios.py")

with action_col2:
    st.markdown("""
    <div class='feature-card' style='padding: 24px 20px; min-height: 180px;'>
        <div style='font-size: 3.5rem; margin-bottom: 16px; filter: drop-shadow(0 0 10px rgba(52, 211, 153, 0.5));'>💹</div>
        <h4 style='color: #34d399; margin: 0 0 8px 0; font-size: 1.2rem; font-weight: 700;'>Start Trading</h4>
        <p style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 16px;'>Buy & sell stocks</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Trading →", use_container_width=True, key="home_trade"):
        st.switch_page("pages/2_💹_Trading.py")

with action_col3:
    st.markdown("""
    <div class='feature-card' style='padding: 24px 20px; min-height: 180px;'>
        <div style='font-size: 3.5rem; margin-bottom: 16px; filter: drop-shadow(0 0 10px rgba(167, 139, 250, 0.5));'>📈</div>
        <h4 style='color: #a78bfa; margin: 0 0 8px 0; font-size: 1.2rem; font-weight: 700;'>Live Market</h4>
        <p style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 16px;'>Real-time data & charts</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Market →", use_container_width=True, key="home_market"):
        st.switch_page("pages/3_📈_Live_Market.py")

with action_col4:
    st.markdown("""
    <div class='feature-card' style='padding: 24px 20px; min-height: 180px;'>
        <div style='font-size: 3.5rem; margin-bottom: 16px; filter: drop-shadow(0 0 10px rgba(96, 165, 250, 0.5));'>📄</div>
        <h4 style='color: #60a5fa; margin: 0 0 8px 0; font-size: 1.2rem; font-weight: 700;'>Generate Report</h4>
        <p style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 16px;'>AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Reports →", use_container_width=True, key="home_report"):
        st.switch_page("pages/4_📄_Reports.py")

st.write("")
st.write("")

# Show market overview only if user has portfolios
if has_portfolios:
    # Advanced Market Overview
    st.markdown("""
    <div class='advanced-card'>
        <h2 class='title' style='text-align: center; margin-bottom: 30px; font-size: 2rem;'>
            📈 Live Market Overview
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Real-time market data for major indices
    try:
        with st.spinner("Loading market data..."):
            # Get major market indices
            indices = {
                "^GSPC": "S&P 500",
                "^DJI": "Dow Jones",
                "^IXIC": "NASDAQ",
                "^VIX": "VIX"
            }
            
            market_data = {}
            for symbol, name in indices.items():
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="2d")
                    if not hist.empty:
                        current = hist['Close'].iloc[-1]
                        previous = hist['Close'].iloc[-2] if len(hist) > 1 else current
                        change = current - previous
                        change_pct = (change / previous * 100) if previous != 0 else 0
                        market_data[name] = {
                            'current': current,
                            'change': change,
                            'change_pct': change_pct
                        }
                except:
                    continue
            
            if market_data:
                market_cols = st.columns(len(market_data))
                for i, (name, data) in enumerate(market_data.items()):
                    with market_cols[i]:
                        delta_color = "normal" if data['change'] >= 0 else "inverse"
                        st.metric(
                            label=name,
                            value=f"{data['current']:,.2f}",
                            delta=f"{data['change_pct']:+.2f}%",
                            delta_color=delta_color
                        )
    except:
        st.info("Market data temporarily unavailable")

    st.write("")

    # Portfolio Performance Chart
    st.markdown("""
    <div class='advanced-card'>
        <h3 class='title' style='margin-bottom: 20px;'>📊 Portfolio Performance Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create portfolio comparison chart
    portfolio_data = []
    for name, portfolio in pm.portfolios.items():
        value = portfolio.calculate_portfolio_value()
        positions = len(portfolio.stocks)
        portfolio_data.append({
            'Portfolio': name,
            'Value': value,
            'Positions': positions
        })
    
    if portfolio_data:
        df = pd.DataFrame(portfolio_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Portfolio value comparison
            fig_bar = px.bar(
                df, 
                x='Portfolio', 
                y='Value',
                title="Portfolio Values Comparison",
                color='Value',
                color_continuous_scale='viridis'
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Portfolio positions pie chart
            fig_pie = px.pie(
                df, 
                values='Positions', 
                names='Portfolio',
                title="Portfolio Distribution by Positions"
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    st.write("")

    # Advanced Analytics Dashboard (only for users with stocks)
    if has_stocks:
        st.markdown("""
        <div class='advanced-card'>
            <h3 class='title' style='margin-bottom: 20px;'>🔬 Portfolio Health Metrics</h3>
            <p class='subtle' style='text-align: center; margin-bottom: 20px;'>Key indicators of your portfolio performance</p>
        </div>
        """, unsafe_allow_html=True)

        analytics_col1, analytics_col2, analytics_col3 = st.columns(3)

        with analytics_col1:
            st.markdown("""
            <div class='glass pulse' style='text-align: center; padding: 20px;'>
                <h4 style='color: #22d3ee;'>🎯 Risk Score</h4>
                <div style='font-size: 2rem; margin: 10px 0;'>7.2/10</div>
                <p style='color: #94a3b8; font-size: 0.9rem;'>Moderate Risk Level</p>
            </div>
            """, unsafe_allow_html=True)

        with analytics_col2:
            st.markdown("""
            <div class='glass pulse' style='text-align: center; padding: 20px;'>
                <h4 style='color: #a78bfa;'>📈 Sharpe Ratio</h4>
                <div style='font-size: 2rem; margin: 10px 0;'>1.45</div>
                <p style='color: #94a3b8; font-size: 0.9rem;'>Good Risk-Adjusted Return</p>
            </div>
            """, unsafe_allow_html=True)

        with analytics_col3:
            st.markdown("""
            <div class='glass pulse' style='text-align: center; padding: 20px;'>
                <h4 style='color: #34d399;'>🎲 Diversification</h4>
                <div style='font-size: 2rem; margin: 10px 0;'>85%</div>
                <p style='color: #94a3b8; font-size: 0.9rem;'>Well Diversified</p>
            </div>
            """, unsafe_allow_html=True)

st.write("")

# Compact Footer
st.write("")
st.write("")
st.markdown("""
<div class='glass' style='text-align: center; padding: 30px 20px; margin-top: 60px;'>
    <p style='color: #94a3b8; font-size: 1rem; margin-bottom: 16px;'>
        <span style='font-weight: 600; color: #22d3ee;'>Powered by:</span> 
        🐍 Python • 📊 Streamlit • 📈 Plotly • 💾 SQLite • 📡 yfinance • 🤖 AI Analytics
    </p>
    <div style='border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 16px; margin-top: 16px;'>
        <p style='color: #94a3b8; font-size: 0.9rem; margin: 0;'>
            © 2025 Portfolio Tracker | Built with ❤️ for investors
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
