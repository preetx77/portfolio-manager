# pages/3_📈_Live_Market.py
import streamlit as st
from portfolio import PortfolioManager
from transaction import Transaction
import database
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# ---------- Page Config ----------
st.set_page_config(
    page_title="Live Market Data",
    page_icon="📈",
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

pm: PortfolioManager = st.session_state.pm

# ---------- Header ----------
st.markdown("<h1 class='title'>📈 Live Market Data</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------- Sidebar Navigation ----------
st.sidebar.header("🚀 Navigation")
with st.sidebar:
    st.page_link("home.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/1_📊_Portfolios.py", label="📊 Portfolios", icon="📊")
    st.page_link("pages/2_💹_Trading.py", label="💹 Trading", icon="💹")
    st.page_link("pages/3_📈_Live_Market.py", label="📈 Live Market", icon="📈")
    st.page_link("pages/4_📄_Reports.py", label="📄 Reports", icon="📄")
    st.page_link("pages/5_ℹ️_About.py", label="ℹ️ About", icon="ℹ️")

# ---------- Live Market Content ----------
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.subheader("Real-time Market Analysis")

# Market Data Controls
sym_input = st.text_input("Stock Symbols (comma separated)", value="AAPL, MSFT, TSLA, GOOGL", key="live_syms")
colA, colB, colC = st.columns(3)
with colA:
    period = st.selectbox("Time Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"], index=2)
with colB:
    interval = st.selectbox("Interval", ["1m", "5m", "15m", "30m", "1h", "1d"], index=5)
with colC:
    go_btn = st.button("📊 Load Market Data", type="primary")

if go_btn and sym_input.strip():
    try:
        with st.spinner("Fetching market data..."):
            tickers = [s.strip().upper() for s in sym_input.split(",") if s.strip()]
            
            # Enhanced error handling and data fetching
            if len(tickers) == 1:
                data = yf.download(tickers[0], period=period, interval=interval, auto_adjust=True, progress=False)
                if not data.empty:
                    data = {tickers[0]: data}
            else:
                data = yf.download(tickers, period=period, interval=interval, group_by='ticker', auto_adjust=True, threads=True, progress=False)

            # Enhanced data processing
            plot_rows = []
            latest_prices = {}
            
            for t in tickers:
                try:
                    if len(tickers) == 1:
                        df = data.get(t, data) if isinstance(data, dict) else data
                    else:
                        df = data[t] if t in data.columns.get_level_values(0) else None
                    
                    if df is None or df.empty:
                        st.warning(f"No data available for {t}")
                        continue
                        
                    df = df.dropna()
                    if df.empty:
                        st.warning(f"No valid data for {t} after cleaning")
                        continue
                        
                    # Get the close price column
                    if 'Close' in df.columns:
                        close_col = df['Close']
                    elif len(df.columns) > 0:
                        close_col = df.iloc[:, -1]  # Use last column if Close not found
                    else:
                        continue
                        
                    latest_prices[t] = float(close_col.iloc[-1])
                    
                    for ts, price in close_col.items():
                        plot_rows.append({
                            "Datetime": ts, 
                            "Symbol": t, 
                            "Close": float(price)
                        })
                except Exception as e:
                    st.error(f"Error processing {t}: {str(e)}")
                    continue

            if not plot_rows:
                st.info("No price data returned for the given inputs.")
            else:
                pdf = pd.DataFrame(plot_rows)
                
                # Market Statistics
                st.markdown("### 📈 Market Overview")
                market_cols = st.columns(len(tickers))
                
                for i, ticker in enumerate(tickers):
                    if ticker in latest_prices:
                        ticker_data = pdf[pdf['Symbol'] == ticker]['Close']
                        if not ticker_data.empty:
                            current_price = latest_prices[ticker]
                            start_price = ticker_data.iloc[0]
                            change = current_price - start_price
                            change_pct = (change / start_price * 100) if start_price != 0 else 0
                            
                            with market_cols[i]:
                                delta_color = "normal" if change >= 0 else "inverse"
                                st.metric(
                                    label=ticker,
                                    value=f"${current_price:,.2f}",
                                    delta=f"{change_pct:+.2f}%",
                                    delta_color=delta_color
                                )
                
                # TradingView-style line chart
                fig = go.Figure()
                
                # TradingView color scheme for different symbols
                tv_colors = ['#2962ff', '#ff6d00', '#00c853', '#e91e63', '#9c27b0', '#ff9800', '#795548']
                
                for i, ticker in enumerate(tickers):
                    ticker_data = pdf[pdf['Symbol'] == ticker]
                    if not ticker_data.empty:
                        fig.add_trace(go.Scatter(
                            x=ticker_data['Datetime'],
                            y=ticker_data['Close'],
                            mode='lines',
                            name=ticker,
                            line=dict(
                                color=tv_colors[i % len(tv_colors)],
                                width=2
                            ),
                            hovertemplate=f'<b>{ticker}</b><br>Price: $%{{y:,.2f}}<br>%{{x}}<extra></extra>'
                        ))
                
                # TradingView styling
                fig.update_layout(
                    title=dict(
                        text="Market Prices - TradingView Style",
                        font=dict(size=16, color="#d1d5db", family="Arial"),
                        x=0.02,
                        y=0.95
                    ),
                    margin=dict(l=60, r=20, t=60, b=40),
                    paper_bgcolor="#1a1a1a",
                    plot_bgcolor="#1a1a1a",
                    font=dict(color="#d1d5db", size=11, family="Arial"),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="left",
                        x=0,
                        bgcolor="rgba(26, 26, 26, 0.8)",
                        bordercolor="#2a2a2a",
                        borderwidth=1
                    ),
                    hovermode='x unified'
                )
                
                fig.update_xaxes(
                    showgrid=True,
                    gridcolor="#2a2a2a",
                    gridwidth=1,
                    tickfont=dict(color="#9ca3af", size=10),
                    title=dict(text="Time", font=dict(color="#9ca3af", size=11))
                )
                
                fig.update_yaxes(
                    showgrid=True,
                    gridcolor="#2a2a2a",
                    gridwidth=1,
                    tickfont=dict(color="#9ca3af", size=10),
                    tickformat="$,.2f",
                    title=dict(text="Price ($)", font=dict(color="#9ca3af", size=11))
                )
                
                st.plotly_chart(fig, use_container_width=True)

                # Market Summary Table
                st.markdown("### 📊 Market Summary")
                summary_data = []
                for ticker in tickers:
                    if ticker in latest_prices:
                        ticker_data = pdf[pdf['Symbol'] == ticker]['Close']
                        if not ticker_data.empty:
                            current_price = latest_prices[ticker]
                            start_price = ticker_data.iloc[0]
                            high_price = ticker_data.max()
                            low_price = ticker_data.min()
                            change = current_price - start_price
                            change_pct = (change / start_price * 100) if start_price != 0 else 0
                            
                            summary_data.append({
                                "Symbol": ticker,
                                "Current": f"${current_price:,.2f}",
                                "Change": f"${change:+,.2f}",
                                "Change %": f"{change_pct:+.2f}%",
                                "High": f"${high_price:,.2f}",
                                "Low": f"${low_price:,.2f}",
                                "Volume": "N/A"
                            })
                
                if summary_data:
                    st.dataframe(summary_data, use_container_width=True, hide_index=True)

        st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Failed to load market data: {str(e)}")
        st.info("💡 **Troubleshooting Tips:**")
        st.markdown("""
        - Check your internet connection
        - Verify stock symbols are correct (e.g., AAPL, MSFT, GOOGL)
        - Try with fewer symbols or different time periods
        - Some symbols may not have data for the selected interval
        """)
        
        # Show sample data as fallback
        st.markdown("### 📊 Sample Market Data")
        sample_data = {
            'Symbol': ['AAPL', 'MSFT', 'GOOGL', 'TSLA'],
            'Price': [150.25, 280.50, 2650.75, 850.30],
            'Change': ['+2.5%', '-1.2%', '+0.8%', '+3.1%'],
            'Volume': ['45.2M', '28.7M', '1.2M', '22.8M']
        }
        st.dataframe(sample_data, use_container_width=True)

# Quick Trade Panel
if 'latest_prices' in locals() and latest_prices and pm.portfolios:
    st.write("")
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("### ⚡ Quick Trade at Market Price")
    
    tcol1, tcol2, tcol3, tcol4, tcol5 = st.columns([1,1,1,1,2])
    with tcol1:
        q_port = st.selectbox("Portfolio", options=list(pm.portfolios.keys()), key="live_port")
    with tcol2:
        q_sym = st.selectbox("Symbol", options=list(latest_prices.keys()), key="live_sym")
    with tcol3:
        q_qty = st.number_input("Quantity", min_value=1, value=1, step=1, key="live_qty")
    with tcol4:
        st.write("**Market Price**")
        st.metric(label="", value=f"${latest_prices.get(q_sym, 0):,.2f}")
    with tcol5:
        c1, c2 = st.columns(2)
        if c1.button("🟢 Buy", key="live_buy", use_container_width=True):
            tx = Transaction(q_sym, 'buy', int(q_qty), float(latest_prices[q_sym]))
            pm.process_transaction(q_port, tx)
            p = pm.get_portfolio(q_port)
            if p:
                database.save_portfolio(p, st.session_state.username)
            st.success(f"✅ Bought {q_qty} {q_sym} @ ${latest_prices[q_sym]:.2f}")
            st.rerun()
        if c2.button("🔴 Sell", key="live_sell", use_container_width=True):
            tx = Transaction(q_sym, 'sell', int(q_qty), float(latest_prices[q_sym]))
            try:
                pm.process_transaction(q_port, tx)
                p = pm.get_portfolio(q_port)
                if p:
                    database.save_portfolio(p, st.session_state.username)
                st.success(f"✅ Sold {q_qty} {q_sym} @ ${latest_prices[q_sym]:.2f}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
            
            st.markdown("</div>", unsafe_allow_html=True)

# Market News Section (Placeholder)
st.write("")
st.markdown("### 📰 Market Insights")
st.info("💡 **Pro Tip**: Use different time periods and intervals to analyze market trends. The 1-day view shows intraday movements, while longer periods reveal broader trends.")

market_tips = [
    "📊 **Technical Analysis**: Look for support and resistance levels in the charts",
    "📈 **Trend Following**: Green trends indicate bullish momentum, red trends show bearish sentiment",
    "⏰ **Timing**: Consider market hours (9:30 AM - 4:00 PM EST) for better liquidity",
    "💰 **Risk Management**: Never invest more than you can afford to lose",
    "🔄 **Diversification**: Spread investments across different sectors and asset classes"
]

for tip in market_tips:
    st.markdown(f"- {tip}")

st.markdown("</div>", unsafe_allow_html=True)

# Quick Navigation
st.write("")
st.markdown("<div class='glass' style='text-align: center; padding: 20px;'>", unsafe_allow_html=True)
st.markdown("### 🚀 Quick Actions")

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    if st.button("💹 Start Trading", use_container_width=True):
        st.switch_page("pages/2_💹_Trading.py")

with nav_col2:
    if st.button("📊 View Portfolios", use_container_width=True):
        st.switch_page("pages/1_📊_Portfolios.py")

with nav_col3:
    if st.button("📄 Generate Report", use_container_width=True):
        st.switch_page("pages/4_📄_Reports.py")

st.markdown("</div>", unsafe_allow_html=True)
