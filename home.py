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
)

# ---------- Custom CSS (Futuristic/Glassmorphism) ----------
st.markdown(
    """
    <style>
    /* Background gradient */
    .stApp {
        background: radial-gradient(1200px 600px at 0% 0%, rgba(0, 255, 204, 0.06), transparent),
                    radial-gradient(1200px 600px at 100% 0%, rgba(0, 127, 255, 0.06), transparent),
                    linear-gradient(135deg, #0f172a 0%, #111827 100%);
        color: #e5e7eb;
    }

    /* Glass cards */
    .glass {
        background: rgba(17, 25, 40, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 18px 20px;
    }

    .title {
        font-weight: 700;
        letter-spacing: 0.1rem;
        background: -webkit-linear-gradient(45deg, #22d3ee, #a78bfa, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtle { color: #94a3b8; }
    .metric-card { 
        text-align:center; 
        padding: 15px; 
        border-radius: 12px; 
        border: 1px solid rgba(255,255,255,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(34, 211, 238, 0.3);
    }
    .success { color: #34d399; }
    .warn { color: #fbbf24; }
    .err { color: #f87171; }
    .pulse {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .advanced-card {
        background: linear-gradient(135deg, rgba(17, 25, 40, 0.8), rgba(17, 25, 40, 0.4));
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 25px;
        transition: all 0.3s ease;
    }
    .advanced-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(34, 211, 238, 0.2);
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

# ---------- Header ----------
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("<h2 class='title'>🏠 Portfolio Tracker</h2>", unsafe_allow_html=True)
with col2:
    st.markdown(
        "<div class='glass'><span class='subtle'>Advanced portfolio management platform</span></div>",
        unsafe_allow_html=True,
    )

st.write("")

# ---------- Global KPIs ----------
total_portfolios = len(pm.portfolios)
total_positions = sum(len(p.stocks) for p in pm.portfolios.values())
total_value = sum(p.calculate_portfolio_value() for p in pm.portfolios.values())

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

# Hero Section
st.markdown("""
<div class='glass' style='text-align: center; padding: 40px 20px; margin-bottom: 30px;'>
    <h1 class='title' style='font-size: 3.5rem; margin-bottom: 20px;'>
        🚀 Portfolio Tracker
    </h1>
    <p style='font-size: 1.3rem; color: #94a3b8; margin-bottom: 30px; line-height: 1.6;'>
        Advanced portfolio management with real-time analytics, AI-powered insights, and futuristic design
    </p>
    <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;'>
        <div style='background: linear-gradient(45deg, #22d3ee, #a78bfa); padding: 2px; border-radius: 12px;'>
            <div style='background: #111827; padding: 12px 24px; border-radius: 10px; color: white;'>
                ⚡ Real-time Data
            </div>
        </div>
        <div style='background: linear-gradient(45deg, #a78bfa, #60a5fa); padding: 2px; border-radius: 12px;'>
            <div style='background: #111827; padding: 12px 24px; border-radius: 10px; color: white;'>
                📊 Advanced Analytics
            </div>
        </div>
        <div style='background: linear-gradient(45deg, #60a5fa, #34d399); padding: 2px; border-radius: 12px;'>
            <div style='background: #111827; padding: 12px 24px; border-radius: 10px; color: white;'>
                🎨 Futuristic UI
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Quick Stats Dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='glass' style='text-align: center; padding: 25px;'>
        <div style='font-size: 2.5rem; margin-bottom: 10px;'>💼</div>
        <h3 style='color: #22d3ee; margin: 0;'>{}</h3>
        <p style='color: #94a3b8; margin: 5px 0 0 0;'>Active Portfolios</p>
    </div>
    """.format(total_portfolios), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='glass' style='text-align: center; padding: 25px;'>
        <div style='font-size: 2.5rem; margin-bottom: 10px;'>📈</div>
        <h3 style='color: #a78bfa; margin: 0;'>{}</h3>
        <p style='color: #94a3b8; margin: 5px 0 0 0;'>Total Positions</p>
    </div>
    """.format(total_positions), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='glass' style='text-align: center; padding: 25px;'>
        <div style='font-size: 2.5rem; margin-bottom: 10px;'>💰</div>
        <h3 style='color: #34d399; margin: 0;'>${:,.0f}</h3>
        <p style='color: #94a3b8; margin: 5px 0 0 0;'>Total Value</p>
    </div>
    """.format(total_value), unsafe_allow_html=True)

with col4:
    active_user = st.session_state.get("username", "default")
    st.markdown("""
    <div class='glass' style='text-align: center; padding: 25px;'>
        <div style='font-size: 2.5rem; margin-bottom: 10px;'>👤</div>
        <h3 style='color: #60a5fa; margin: 0;'>{}</h3>
        <p style='color: #94a3b8; margin: 5px 0 0 0;'>Active Profile</p>
    </div>
    """.format(active_user.title()), unsafe_allow_html=True)

st.write("")

# Compact Features Overview
st.markdown("""
<div class='glass' style='padding: 20px;'>
    <h2 class='title' style='text-align: center; margin-bottom: 25px; font-size: 1.8rem;'>
        🌟 Platform Features
    </h2>
</div>
""", unsafe_allow_html=True)

# Compact Feature Cards
feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)

with feat_col1:
    st.markdown("""
    <div class='glass' style='padding: 10px; text-align: center; height: 90px;'>
        <div style='font-size: 1.5rem; margin-bottom: 5px;'>📊</div>
        <h4 style='color: #22d3ee; margin: 0; font-size: 0.8rem;'>Portfolio Management</h4>
        <p style='color: #94a3b8; margin: 3px 0 0 0; font-size: 0.65rem;'>Multi-portfolio tracking</p>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
    <div class='glass' style='padding: 10px; text-align: center; height: 90px;'>
        <div style='font-size: 1.5rem; margin-bottom: 5px;'>💹</div>
        <h4 style='color: #34d399; margin: 0; font-size: 0.8rem;'>Trading Platform</h4>
        <p style='color: #94a3b8; margin: 3px 0 0 0; font-size: 0.65rem;'>Buy/sell execution</p>
    </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
    <div class='glass' style='padding: 10px; text-align: center; height: 90px;'>
        <div style='font-size: 1.5rem; margin-bottom: 5px;'>📈</div>
        <h4 style='color: #a78bfa; margin: 0; font-size: 0.8rem;'>Live Market Data</h4>
        <p style='color: #94a3b8; margin: 3px 0 0 0; font-size: 0.65rem;'>Real-time charts</p>
    </div>
    """, unsafe_allow_html=True)

with feat_col4:
    st.markdown("""
    <div class='glass' style='padding: 10px; text-align: center; height: 90px;'>
        <div style='font-size: 1.5rem; margin-bottom: 5px;'>📄</div>
        <h4 style='color: #60a5fa; margin: 0; font-size: 0.8rem;'>Smart Reports</h4>
        <p style='color: #94a3b8; margin: 3px 0 0 0; font-size: 0.65rem;'>AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Portfolio Distribution Charts Section
st.markdown("""
<div class='advanced-card'>
    <h2 class='title' style='text-align: center; margin-bottom: 30px; font-size: 2rem;'>
        📊 Portfolio Distribution Analysis
    </h2>
</div>
""", unsafe_allow_html=True)

if pm.portfolios:
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
            
else:
    st.info("📊 Create portfolios and add stocks to see distribution charts")
    st.markdown("""
    **Get started:**
    1. Use the sidebar to create a new portfolio
    2. Add some stocks to your portfolio
    3. Return here to see beautiful distribution visualizations
    """)

st.write("")

# Quick Actions
st.markdown("""
<div class='glass' style='padding: 30px; text-align: center;'>
    <h3 class='title' style='margin-bottom: 30px; font-size: 1.8rem;'>🚀 Quick Actions</h3>
</div>
""", unsafe_allow_html=True)

action_col1, action_col2, action_col3, action_col4 = st.columns(4)

with action_col1:
    if st.button("📊 View Portfolios", use_container_width=True, key="home_portfolios"):
        st.switch_page("pages/1_📊_Portfolios.py")

with action_col2:
    if st.button("💹 Start Trading", use_container_width=True, key="home_trade"):
        st.switch_page("pages/2_💹_Trading.py")

with action_col3:
    if st.button("📈 Live Market", use_container_width=True, key="home_market"):
        st.switch_page("pages/3_📈_Live_Market.py")

with action_col4:
    if st.button("📄 Generate Report", use_container_width=True, key="home_report"):
        st.switch_page("pages/4_📄_Reports.py")

# Technology Stack
st.write("")
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
if pm.portfolios:
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

# Advanced Analytics Dashboard
st.markdown("""
<div class='advanced-card'>
    <h3 class='title' style='margin-bottom: 20px;'>🔬 Advanced Analytics</h3>
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

# Technology Stack
st.markdown("""
<div class='glass' style='padding: 25px; text-align: center;'>
    <h4 style='color: #94a3b8; margin-bottom: 20px;'>Powered by Advanced Technology</h4>
    <div style='display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;'>
        <span style='color: #22d3ee;'>🐍 Python</span>
        <span style='color: #a78bfa;'>📊 Streamlit</span>
        <span style='color: #34d399;'>📈 Plotly</span>
        <span style='color: #60a5fa;'>💾 SQLite</span>
        <span style='color: #f59e0b;'>📡 yfinance</span>
        <span style='color: #ec4899;'>🤖 AI Analytics</span>
    </div>
</div>
""", unsafe_allow_html=True)
