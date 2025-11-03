# pages/6_📊_Charts.py - Advanced Portfolio Charts & Analytics
import streamlit as st
from portfolio import PortfolioManager
import database
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ---------- Page Config ----------
st.set_page_config(
    page_title="Portfolio Charts & Analytics",
    page_icon="📊",
    layout="wide",
)

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(1200px 600px at 0% 0%, rgba(0, 255, 204, 0.06), transparent),
                    radial-gradient(1200px 600px at 100% 0%, rgba(0, 127, 255, 0.06), transparent),
                    linear-gradient(135deg, #0f172a 0%, #111827 100%);
        color: #e5e7eb;
    }
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
    .chart-card {
        background: rgba(17, 25, 40, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
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
    st.session_state.username = "default"

# Initialize chart data session state
if "chart_data" not in st.session_state:
    st.session_state.chart_data = None
if "chart_period" not in st.session_state:
    st.session_state.chart_period = "1mo"
if "chart_interval" not in st.session_state:
    st.session_state.chart_interval = "1d"

pm: PortfolioManager = st.session_state.pm

# ---------- Sidebar Navigation ----------
st.sidebar.header("🚀 Navigation")
with st.sidebar:
    st.page_link("home.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/1_📊_Portfolios.py", label="📊 Portfolios", icon="📊")
    st.page_link("pages/2_💹_Trading.py", label="💹 Trading", icon="💹")
    st.page_link("pages/3_📈_Live_Market.py", label="📈 Live Market", icon="📈")
    st.page_link("pages/4_📄_Reports.py", label="📄 Reports", icon="📄")
    st.page_link("pages/5_ℹ️_About.py", label="ℹ️ About", icon="ℹ️")
    st.page_link("pages/6_📊_Charts.py", label="📊 Charts", icon="📊")

# ---------- Header ----------
st.markdown("<h1 class='title'>📊 Advanced Portfolio Charts</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------- Chart Type Selection ----------
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.subheader("📈 Chart Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    chart_type = st.selectbox(
        "Chart Type",
        ["Price Chart", "Candlestick Chart", "Volume Chart", "Comparison Chart", "Portfolio Performance"],
        key="chart_type_select"
    )

with col2:
    period_options = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"]
    period = st.selectbox("Time Period", period_options, index=2, key="period_select")

with col3:
    interval_options = ["1m", "5m", "15m", "30m", "1h", "1d", "1wk", "1mo"]
    interval = st.selectbox("Interval", interval_options, index=5, key="interval_select")

st.markdown("</div>", unsafe_allow_html=True)
st.write("")

# ---------- Stock/Portfolio Selection ----------
st.markdown("<div class='glass'>", unsafe_allow_html=True)

if chart_type == "Portfolio Performance":
    st.subheader("📊 Select Portfolio")
    if pm.portfolios:
        selected_portfolio = st.selectbox(
            "Portfolio",
            options=list(pm.portfolios.keys()),
            key="portfolio_select"
        )
    else:
        st.warning("No portfolios available. Create a portfolio first.")
        selected_portfolio = None
else:
    st.subheader("📈 Select Stocks")
    
    # Option to select from portfolio stocks or enter custom symbols
    selection_mode = st.radio(
        "Selection Mode",
        ["From Portfolio", "Custom Symbols"],
        horizontal=True,
        key="selection_mode"
    )
    
    if selection_mode == "From Portfolio":
        if pm.portfolios:
            portfolio_for_stocks = st.selectbox(
                "Select Portfolio",
                options=list(pm.portfolios.keys()),
                key="portfolio_for_stocks"
            )
            portfolio = pm.get_portfolio(portfolio_for_stocks)
            if portfolio and portfolio.stocks:
                stock_symbols = list(portfolio.stocks.keys())
                selected_symbols = st.multiselect(
                    "Select Stocks",
                    options=stock_symbols,
                    default=stock_symbols[:min(4, len(stock_symbols))],
                    key="portfolio_stocks_select"
                )
            else:
                st.warning("No stocks in selected portfolio.")
                selected_symbols = []
        else:
            st.warning("No portfolios available.")
            selected_symbols = []
    else:
        symbols_input = st.text_input(
            "Stock Symbols (comma separated)",
            value="AAPL, MSFT, GOOGL, TSLA",
            key="custom_symbols_input"
        )
        selected_symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]

load_chart_btn = st.button("📊 Generate Chart", type="primary", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
st.write("")

# ---------- Validation Function ----------
def validate_period_interval(period, interval):
    """Validate if period/interval combination is supported by yfinance"""
    period_days = {
        "1d": 1, "5d": 5, "1mo": 30, "3mo": 90,
        "6mo": 180, "1y": 365, "2y": 730, "5y": 1825
    }
    
    interval_limits = {
        "1m": 7, "5m": 60, "15m": 60, "30m": 60,
        "1h": 730, "1d": 9999, "1wk": 9999, "1mo": 9999
    }
    
    selected_days = period_days.get(period, 0)
    max_days = interval_limits.get(interval, 0)
    
    if selected_days > max_days:
        return False, f"Interval '{interval}' only supports up to {max_days} days."
    return True, ""

# ---------- Chart Generation ----------
if load_chart_btn:
    if chart_type == "Portfolio Performance" and not selected_portfolio:
        st.error("Please select a portfolio.")
    elif chart_type != "Portfolio Performance" and not selected_symbols:
        st.error("Please select at least one stock symbol.")
    else:
        is_valid, error_msg = validate_period_interval(period, interval)
        if not is_valid:
            st.error(f"Invalid period/interval combination: {error_msg}")
        else:
            try:
                with st.spinner("Generating chart..."):
                    
                    # ========== PRICE CHART ==========
                    if chart_type == "Price Chart":
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.markdown("### 📈 Price Chart")
                        
                        fig = go.Figure()
                        colors = ['#2962ff', '#ff6d00', '#00c853', '#e91e63', '#9c27b0', '#ff9800']
                        
                        for idx, symbol in enumerate(selected_symbols):
                            data = yf.download(symbol, period=period, interval=interval, progress=False)
                            if not data.empty and 'Close' in data.columns:
                                fig.add_trace(go.Scatter(
                                    x=data.index,
                                    y=data['Close'],
                                    mode='lines',
                                    name=symbol,
                                    line=dict(color=colors[idx % len(colors)], width=2),
                                    hovertemplate=f'<b>{symbol}</b><br>Price: $%{{y:,.2f}}<br>%{{x}}<extra></extra>'
                                ))
                        
                        fig.update_layout(
                            title="Stock Price Trends",
                            xaxis_title="Date",
                            yaxis_title="Price ($)",
                            hovermode='x unified',
                            paper_bgcolor='#1a1a1a',
                            plot_bgcolor='#1a1a1a',
                            font=dict(color='#d1d5db'),
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
                        )
                        fig.update_xaxes(showgrid=True, gridcolor='#2a2a2a')
                        fig.update_yaxes(showgrid=True, gridcolor='#2a2a2a')
                        
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # ========== CANDLESTICK CHART ==========
                    elif chart_type == "Candlestick Chart":
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.markdown("### 🕯️ Candlestick Chart")
                        
                        # Candlestick works best with single stock
                        symbol = selected_symbols[0] if selected_symbols else "AAPL"
                        data = yf.download(symbol, period=period, interval=interval, progress=False)
                        
                        if not data.empty:
                            fig = go.Figure(data=[go.Candlestick(
                                x=data.index,
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                name=symbol
                            )])
                            
                            fig.update_layout(
                                title=f"{symbol} Candlestick Chart",
                                xaxis_title="Date",
                                yaxis_title="Price ($)",
                                paper_bgcolor='#1a1a1a',
                                plot_bgcolor='#1a1a1a',
                                font=dict(color='#d1d5db'),
                                xaxis_rangeslider_visible=False
                            )
                            fig.update_xaxes(showgrid=True, gridcolor='#2a2a2a')
                            fig.update_yaxes(showgrid=True, gridcolor='#2a2a2a')
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Add technical indicators
                            st.markdown("#### 📊 Technical Indicators")
                            data['SMA_20'] = data['Close'].rolling(window=20).mean()
                            data['SMA_50'] = data['Close'].rolling(window=50).mean()
                            
                            fig2 = go.Figure()
                            fig2.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close', line=dict(color='#2962ff')))
                            fig2.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20', line=dict(color='#ff6d00', dash='dash')))
                            fig2.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='SMA 50', line=dict(color='#00c853', dash='dash')))
                            
                            fig2.update_layout(
                                title="Moving Averages",
                                xaxis_title="Date",
                                yaxis_title="Price ($)",
                                paper_bgcolor='#1a1a1a',
                                plot_bgcolor='#1a1a1a',
                                font=dict(color='#d1d5db'),
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
                            )
                            fig2.update_xaxes(showgrid=True, gridcolor='#2a2a2a')
                            fig2.update_yaxes(showgrid=True, gridcolor='#2a2a2a')
                            
                            st.plotly_chart(fig2, use_container_width=True)
                        else:
                            st.warning(f"No data available for {symbol}")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # ========== VOLUME CHART ==========
                    elif chart_type == "Volume Chart":
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.markdown("### 📊 Volume Analysis")
                        
                        symbol = selected_symbols[0] if selected_symbols else "AAPL"
                        data = yf.download(symbol, period=period, interval=interval, progress=False)
                        
                        if not data.empty and 'Volume' in data.columns:
                            # Create subplot with price and volume
                            fig = make_subplots(
                                rows=2, cols=1,
                                shared_xaxes=True,
                                vertical_spacing=0.03,
                                subplot_titles=(f'{symbol} Price', 'Volume'),
                                row_heights=[0.7, 0.3]
                            )
                            
                            # Price chart
                            fig.add_trace(
                                go.Scatter(x=data.index, y=data['Close'], name='Price', line=dict(color='#2962ff')),
                                row=1, col=1
                            )
                            
                            # Volume chart
                            colors_vol = ['#00c853' if data['Close'].iloc[i] >= data['Open'].iloc[i] else '#f44336' 
                                         for i in range(len(data))]
                            fig.add_trace(
                                go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color=colors_vol),
                                row=2, col=1
                            )
                            
                            fig.update_layout(
                                height=700,
                                paper_bgcolor='#1a1a1a',
                                plot_bgcolor='#1a1a1a',
                                font=dict(color='#d1d5db'),
                                showlegend=False
                            )
                            fig.update_xaxes(showgrid=True, gridcolor='#2a2a2a')
                            fig.update_yaxes(showgrid=True, gridcolor='#2a2a2a')
                            
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning(f"No volume data available for {symbol}")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # ========== COMPARISON CHART ==========
                    elif chart_type == "Comparison Chart":
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.markdown("### 📊 Stock Comparison (Normalized)")
                        
                        fig = go.Figure()
                        colors = ['#2962ff', '#ff6d00', '#00c853', '#e91e63', '#9c27b0', '#ff9800']
                        
                        for idx, symbol in enumerate(selected_symbols):
                            data = yf.download(symbol, period=period, interval=interval, progress=False)
                            if not data.empty and 'Close' in data.columns:
                                # Normalize to percentage change from start
                                normalized = (data['Close'] / data['Close'].iloc[0] - 1) * 100
                                fig.add_trace(go.Scatter(
                                    x=data.index,
                                    y=normalized,
                                    mode='lines',
                                    name=symbol,
                                    line=dict(color=colors[idx % len(colors)], width=2),
                                    hovertemplate=f'<b>{symbol}</b><br>Change: %{{y:.2f}}%<br>%{{x}}<extra></extra>'
                                ))
                        
                        fig.update_layout(
                            title="Normalized Stock Performance",
                            xaxis_title="Date",
                            yaxis_title="Change (%)",
                            hovermode='x unified',
                            paper_bgcolor='#1a1a1a',
                            plot_bgcolor='#1a1a1a',
                            font=dict(color='#d1d5db'),
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
                        )
                        fig.update_xaxes(showgrid=True, gridcolor='#2a2a2a')
                        fig.update_yaxes(showgrid=True, gridcolor='#2a2a2a')
                        
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # ========== PORTFOLIO PERFORMANCE ==========
                    elif chart_type == "Portfolio Performance":
                        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                        st.markdown(f"### 💼 Portfolio Performance: {selected_portfolio}")
                        
                        portfolio = pm.get_portfolio(selected_portfolio)
                        if portfolio and portfolio.stocks:
                            # Get all symbols in portfolio
                            symbols = list(portfolio.stocks.keys())
                            
                            # Create portfolio value over time
                            portfolio_values = []
                            dates = None
                            
                            for symbol in symbols:
                                stock_data = portfolio.stocks[symbol]
                                quantity = stock_data['quantity']
                                
                                hist_data = yf.download(symbol, period=period, interval=interval, progress=False)
                                if not hist_data.empty and 'Close' in hist_data.columns:
                                    if dates is None:
                                        dates = hist_data.index
                                    portfolio_values.append(hist_data['Close'] * quantity)
                            
                            if portfolio_values and dates is not None:
                                # Sum all stock values
                                total_portfolio_value = pd.concat(portfolio_values, axis=1).sum(axis=1)
                                
                                # Create chart
                                fig = go.Figure()
                                fig.add_trace(go.Scatter(
                                    x=dates,
                                    y=total_portfolio_value,
                                    mode='lines',
                                    name='Portfolio Value',
                                    line=dict(color='#2962ff', width=3),
                                    fill='tozeroy',
                                    fillcolor='rgba(41, 98, 255, 0.1)',
                                    hovertemplate='Value: $%{y:,.2f}<br>%{x}<extra></extra>'
                                ))
                                
                                fig.update_layout(
                                    title=f"{selected_portfolio} - Total Value Over Time",
                                    xaxis_title="Date",
                                    yaxis_title="Portfolio Value ($)",
                                    paper_bgcolor='#1a1a1a',
                                    plot_bgcolor='#1a1a1a',
                                    font=dict(color='#d1d5db')
                                )
                                fig.update_xaxes(showgrid=True, gridcolor='#2a2a2a')
                                fig.update_yaxes(showgrid=True, gridcolor='#2a2a2a')
                                
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Portfolio composition pie chart
                                st.markdown("#### 📊 Current Portfolio Composition")
                                composition_data = []
                                for symbol, stock_data in portfolio.stocks.items():
                                    value = stock_data['stock'].price * stock_data['quantity']
                                    composition_data.append({'Symbol': symbol, 'Value': value})
                                
                                comp_df = pd.DataFrame(composition_data)
                                fig_pie = px.pie(
                                    comp_df,
                                    values='Value',
                                    names='Symbol',
                                    title='Portfolio Allocation',
                                    color_discrete_sequence=px.colors.qualitative.Set3
                                )
                                fig_pie.update_layout(
                                    paper_bgcolor='#1a1a1a',
                                    font=dict(color='#d1d5db')
                                )
                                st.plotly_chart(fig_pie, use_container_width=True)
                            else:
                                st.warning("Unable to fetch historical data for portfolio stocks.")
                        else:
                            st.warning("Portfolio is empty.")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error generating chart: {str(e)}")
                st.info("💡 Try selecting different stocks or time periods.")

# ---------- Chart Tips ----------
st.write("")
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("### 💡 Chart Tips")

tips = {
    "Price Chart": "Track price movements of multiple stocks simultaneously",
    "Candlestick Chart": "Analyze OHLC (Open, High, Low, Close) data with technical indicators",
    "Volume Chart": "Understand trading volume patterns and price-volume relationships",
    "Comparison Chart": "Compare relative performance of different stocks (normalized)",
    "Portfolio Performance": "Monitor your entire portfolio value over time"
}

for chart, tip in tips.items():
    st.markdown(f"- **{chart}**: {tip}")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- Quick Navigation ----------
st.write("")
st.markdown("<div class='glass' style='text-align: center; padding: 20px;'>", unsafe_allow_html=True)
st.markdown("### 🚀 Quick Actions")

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    if st.button("📈 Live Market", use_container_width=True):
        st.switch_page("pages/3_📈_Live_Market.py")

with nav_col2:
    if st.button("📊 Portfolios", use_container_width=True):
        st.switch_page("pages/1_📊_Portfolios.py")

with nav_col3:
    if st.button("💹 Trading", use_container_width=True):
        st.switch_page("pages/2_💹_Trading.py")

st.markdown("</div>", unsafe_allow_html=True)
