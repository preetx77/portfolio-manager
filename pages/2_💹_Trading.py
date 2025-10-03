# pages/2_💹_Trading.py
import streamlit as st
from portfolio import PortfolioManager
from transaction import Transaction
import database

# ---------- Page Config ----------
st.set_page_config(
    page_title="Trading Platform",
    page_icon="💹",
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
st.markdown("<h1 class='title'>💹 Trading Platform</h1>", unsafe_allow_html=True)
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

# ---------- Trading Content ----------
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.subheader("Execute Trades")

if not pm.portfolios:
    st.info("Create a portfolio first to start trading.")
else:
    # Trading Interface
    colL, colR = st.columns(2)

    with colL:
        st.markdown("#### 🟢 Buy Orders")
        st.markdown("<div class='glass' style='padding: 20px; margin: 10px 0;'>", unsafe_allow_html=True)
        
        pname_b = st.selectbox("Portfolio", options=list(pm.portfolios.keys()), key="buy_port")
        sym_b = st.text_input("Stock Symbol", key="buy_sym", placeholder="e.g., AAPL")
        qty_b = st.number_input("Quantity", min_value=1, value=1, step=1, key="buy_qty")
        price_b = st.number_input("Price per share ($)", min_value=0.0, value=100.0, step=0.01, key="buy_price")
        
        # Calculate total cost
        total_cost = qty_b * price_b
        st.info(f"Total Cost: ${total_cost:,.2f}")
        
        if st.button("🚀 Execute Buy Order", type="primary", use_container_width=True):
            if sym_b.strip():
                tx = Transaction(sym_b.strip().upper(), 'buy', int(qty_b), float(price_b))
                pm.process_transaction(pname_b, tx)
                p = pm.get_portfolio(pname_b)
                if p:
                    database.save_portfolio(p, st.session_state.username)
                st.success(f"✅ Bought {qty_b} shares of {sym_b.upper()} @ ${price_b:.2f} in {pname_b}")
                st.balloons()
            else:
                st.error("Please enter a valid stock symbol")
        
        st.markdown("</div>", unsafe_allow_html=True)

    with colR:
        st.markdown("#### 🔴 Sell Orders")
        st.markdown("<div class='glass' style='padding: 20px; margin: 10px 0;'>", unsafe_allow_html=True)
        
        pname_s = st.selectbox("Portfolio", options=list(pm.portfolios.keys()), key="sell_port")
        
        # Show available stocks in selected portfolio
        selected_portfolio = pm.get_portfolio(pname_s)
        if selected_portfolio and selected_portfolio.stocks:
            available_stocks = list(selected_portfolio.stocks.keys())
            sym_s = st.selectbox("Stock Symbol", options=available_stocks, key="sell_sym_select")
            
            # Show current holdings
            if sym_s in selected_portfolio.stocks:
                current_qty = selected_portfolio.stocks[sym_s]['quantity']
                current_price = selected_portfolio.stocks[sym_s]['stock'].price
                st.info(f"Current Holdings: {current_qty} shares @ ${current_price:.2f}")
        else:
            sym_s = st.text_input("Stock Symbol", key="sell_sym", placeholder="e.g., AAPL")
        
        qty_s = st.number_input("Quantity", min_value=1, value=1, step=1, key="sell_qty")
        price_s = st.number_input("Price per share ($)", min_value=0.0, value=100.0, step=0.01, key="sell_price")
        
        # Calculate total proceeds
        total_proceeds = qty_s * price_s
        st.info(f"Total Proceeds: ${total_proceeds:,.2f}")
        
        if st.button("📉 Execute Sell Order", use_container_width=True):
            if sym_s and sym_s.strip():
                tx = Transaction(sym_s.strip().upper(), 'sell', int(qty_s), float(price_s))
                try:
                    pm.process_transaction(pname_s, tx)
                    p = pm.get_portfolio(pname_s)
                    if p:
                        database.save_portfolio(p, st.session_state.username)
                    st.success(f"✅ Sold {qty_s} shares of {sym_s.upper()} @ ${price_s:.2f} from {pname_s}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.error("Please select or enter a valid stock symbol")
        
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Trading History Section
st.write("")
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.subheader("📋 Portfolio Overview")

if pm.portfolios:
    # Show portfolio summaries
    for portfolio_name, portfolio in pm.portfolios.items():
        with st.expander(f"📊 {portfolio_name} - ${portfolio.calculate_portfolio_value():,.2f}"):
            if portfolio.stocks:
                portfolio_data = []
                for symbol, data in portfolio.stocks.items():
                    stock = data['stock']
                    quantity = data['quantity']
                    if stock.symbol and stock.symbol.strip():
                        portfolio_data.append({
                            "Symbol": stock.symbol.upper(),
                            "Quantity": quantity,
                            "Price": f"${stock.price:.2f}",
                            "Value": f"${stock.price * quantity:,.2f}"
                        })
                
                if portfolio_data:
                    st.dataframe(portfolio_data, use_container_width=True, hide_index=True)
                else:
                    st.info("No stocks in this portfolio")
            else:
                st.info("No stocks in this portfolio")

st.markdown("</div>", unsafe_allow_html=True)

# Quick Actions
st.write("")
st.markdown("<div class='glass' style='text-align: center; padding: 20px;'>", unsafe_allow_html=True)
st.markdown("### 🚀 Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("📊 View Portfolios", use_container_width=True):
        st.switch_page("pages/1_📊_Portfolios.py")

with action_col2:
    if st.button("📈 Live Market", use_container_width=True):
        st.switch_page("pages/3_📈_Live_Market.py")

with action_col3:
    if st.button("📄 Generate Report", use_container_width=True):
        st.switch_page("pages/4_📄_Reports.py")

st.markdown("</div>", unsafe_allow_html=True)
