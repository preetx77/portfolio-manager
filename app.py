# app.py
import streamlit as st
from portfolio import PortfolioManager
from transaction import Transaction
from report import ReportGenerator
import database
import plotly.express as px
import yfinance as yf

# ---------- Page Config ----------
st.set_page_config(
    page_title="Stock Portfolio Tracker",
    page_icon="💹",
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

    .metric-card { text-align:center; padding: 10px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); }

    .success { color: #34d399; }
    .warn { color: #fbbf24; }
    .err { color: #f87171; }
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
    st.markdown("<h2 class='title'>💹 Portfolio Tracker</h2>", unsafe_allow_html=True)
with col2:
    st.markdown(
        "<div class='glass'><span class='subtle'>Manage portfolios • Add/Buy/Sell stocks • Generate reports</span></div>",
        unsafe_allow_html=True,
    )

st.write("")

# ---------- Global KPIs ----------
total_portfolios = len(pm.portfolios)
total_positions = sum(len(p.stocks) for p in pm.portfolios.values())
total_value = sum(p.calculate_portfolio_value() for p in pm.portfolios.values())

k1, k2, k3 = st.columns(3)
with k1:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.metric("Portfolios", f"{total_portfolios}")
    st.markdown("</div>", unsafe_allow_html=True)
with k2:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.metric("Positions", f"{total_positions}")
    st.markdown("</div>", unsafe_allow_html=True)
with k3:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.metric("Total Value", f"${total_value:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Sidebar: Profile & Actions ----------
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

st.sidebar.header("Actions")
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

# ---------- Tabs ----------
tab_home, tab_portfolios, tab_trade, tab_live, tab_report, tab_about = st.tabs([
    "🏠 Home", "📊 Portfolios", "💹 Trade", "📈 Live Market", "📄 Reports", "ℹ️ About"
])

# ----- Home Tab -----
with tab_home:
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
    
    # Features Showcase
    st.markdown("""
    <div class='glass' style='padding: 30px;'>
        <h2 class='title' style='text-align: center; margin-bottom: 40px; font-size: 2.2rem;'>
            🌟 Platform Features
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    feat_col1, feat_col2 = st.columns(2)
    
    with feat_col1:
        st.markdown("""
        <div class='glass' style='padding: 15px; margin-bottom: 15px; height: 180px;'>
            <div style='display: flex; align-items: center; margin-bottom: 12px;'>
                <div style='font-size: 2rem; margin-right: 12px;'>📊</div>
                <div>
                    <h4 style='color: #22d3ee; margin: 0; font-size: 0.9rem;'>Portfolio Management</h4>
                    <p style='color: #94a3b8; margin: 3px 0 0 0; font-size: 0.7rem;'>Advanced Analytics</p>
                </div>
            </div>
            <ul style='color: #e5e7eb; line-height: 1.4; list-style: none; padding: 0; font-size: 0.75rem;'>
                <li>🔹 Multi-portfolio tracking</li>
                <li>🔹 Real-time monitoring</li>
                <li>🔹 Interactive charts</li>
                <li>🔹 Performance metrics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass' style='padding: 15px; height: 180px;'>
            <div style='display: flex; align-items: center; margin-bottom: 12px;'>
                <div style='font-size: 2rem; margin-right: 12px;'>📈</div>
                <div>
                    <h4 style='color: #a78bfa; margin: 0; font-size: 0.9rem;'>Live Market Data</h4>
                    <p style='color: #94a3b8; margin: 3px 0 0 0; font-size: 0.7rem;'>Real-time Trading</p>
                </div>
            </div>
            <ul style='color: #e5e7eb; line-height: 1.4; list-style: none; padding: 0; font-size: 0.75rem;'>
                <li>🔹 TradingView charts</li>
                <li>🔹 Multiple timeframes</li>
                <li>🔹 Live price updates</li>
                <li>🔹 Quick execution</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown("""
        <div class='glass' style='padding: 15px; margin-bottom: 15px; height: 180px;'>
            <div style='display: flex; align-items: center; margin-bottom: 12px;'>
                <div style='font-size: 2rem; margin-right: 12px;'>💹</div>
                <div>
                    <h4 style='color: #34d399; margin: 0; font-size: 0.9rem;'>Trading Platform</h4>
                    <p style='color: #94a3b8; margin: 3px 0 0 0; font-size: 0.7rem;'>Buy & Sell Stocks</p>
                </div>
            </div>
            <ul style='color: #e5e7eb; line-height: 1.4; list-style: none; padding: 0; font-size: 0.75rem;'>
                <li>🔹 Instant buy/sell orders</li>
                <li>🔹 Custom price execution</li>
                <li>🔹 Transaction history</li>
                <li>🔹 Portfolio rebalancing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass' style='padding: 15px; height: 180px;'>
            <div style='display: flex; align-items: center; margin-bottom: 12px;'>
                <div style='font-size: 2rem; margin-right: 12px;'>📄</div>
                <div>
                    <h4 style='color: #60a5fa; margin: 0; font-size: 0.9rem;'>Smart Reports</h4>
                    <p style='color: #94a3b8; margin: 3px 0 0 0; font-size: 0.7rem;'>AI-Powered Insights</p>
                </div>
            </div>
            <ul style='color: #e5e7eb; line-height: 1.4; list-style: none; padding: 0; font-size: 0.75rem;'>
                <li>🔹 Automated generation</li>
                <li>🔹 Performance analysis</li>
                <li>🔹 Risk assessment</li>
                <li>🔹 Export capabilities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
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
            st.session_state.active_tab = "portfolios"
            st.rerun()
    
    with action_col2:
        if st.button("💹 Start Trading", use_container_width=True, key="home_trade"):
            st.session_state.active_tab = "trade"
            st.rerun()
    
    with action_col3:
        if st.button("📈 Live Market", use_container_width=True, key="home_market"):
            st.session_state.active_tab = "live"
            st.rerun()
    
    with action_col4:
        if st.button("📄 Generate Report", use_container_width=True, key="home_report"):
            st.session_state.active_tab = "report"
            st.rerun()
    
    # Technology Stack
    st.write("")
    st.markdown("""
    <div class='glass' style='padding: 25px; text-align: center;'>
        <h4 style='color: #94a3b8; margin-bottom: 20px;'>Powered by Advanced Technology</h4>
        <div style='display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;'>
            <span style='color: #22d3ee;'>🐍 Python</span>
            <span style='color: #a78bfa;'>📊 Streamlit</span>
            <span style='color: #34d399;'>📈 Plotly</span>
            <span style='color: #60a5fa;'>💾 SQLite</span>
            <span style='color: #f59e0b;'>📡 yfinance</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----- Portfolios Tab -----
with tab_portfolios:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("Your Portfolios")

    if not pm.portfolios:
        st.info("No portfolios yet. Use 'Add Portfolio' in the sidebar to create one.")
    else:
        names = list(pm.portfolios.keys())
        cols = st.columns(3)
        for i, name in enumerate(names):
            with cols[i % 3]:
                p = pm.get_portfolio(name)
                total_value = p.calculate_portfolio_value()
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric(label=f"{name}", value=f"${total_value:,.2f}")
                st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        select_name = st.selectbox("View details for", options=names, key="detail_port")
        p = pm.get_portfolio(select_name)
        if p:
            st.write(f"Portfolio: {p.name}")
            if p.stocks:
                data = []
                for s, d in p.stocks.items():
                    stock = d['stock']
                    qty = d['quantity']
                    # Skip if symbol is empty or invalid
                    if not stock.symbol or stock.symbol.strip() == '':
                        continue
                    data.append({
                        "Symbol": stock.symbol.strip().upper(),
                        "Name": stock.name,
                        "Price": round(stock.price, 2),
                        "Quantity": qty,
                        "Value": round(stock.price * qty, 2),
                    })
                st.dataframe(data, use_container_width=True, hide_index=True)

                # Simple Portfolio Statistics
                st.markdown("### 📊 Portfolio Summary")
                
                # Calculate basic stats
                total_value = sum(row["Value"] for row in data)
                total_positions = len(data)
                
                # Display key metrics in simple format
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Value", f"${total_value:,.2f}")
                with col2:
                    st.metric("Total Positions", total_positions)
                with col3:
                    if data:
                        largest = max(data, key=lambda x: x["Value"])
                        st.metric("Top Holding", largest["Symbol"])
                with col4:
                    if total_positions > 0:
                        avg_value = total_value / total_positions
                        st.metric("Avg Position", f"${avg_value:,.2f}")

                # Simple breakdown table
                st.markdown("### 📈 Position Breakdown")
                
                # Sort data by value
                sorted_data = sorted(data, key=lambda x: x["Value"], reverse=True)
                
                # Create simple breakdown
                breakdown = []
                for i, row in enumerate(sorted_data):
                    pct = (row["Value"] / total_value * 100) if total_value > 0 else 0
                    breakdown.append({
                        "Rank": i + 1,
                        "Symbol": row["Symbol"],
                        "Shares": f"{row['Quantity']:,}",
                        "Price": f"${row['Price']:,.2f}",
                        "Value": f"${row['Value']:,.2f}",
                        "Weight": f"{pct:.1f}%"
                    })
                
                # Display simple table
                st.table(breakdown)

                # Portfolio Allocation Charts
                st.markdown("### 📊 Portfolio Allocation Charts")
                
                # Get data for charts
                labels = [row["Symbol"] for row in sorted_data]
                values = [row["Value"] for row in sorted_data]
                
                if labels and values:
                    # Create two columns for pie and bar charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Colorful Pie Chart
                        import plotly.express as px
                        
                        pie_fig = px.pie(
                            names=labels,
                            values=values,
                            title="Portfolio Allocation",
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        pie_fig.update_traces(
                            textposition='inside',
                            textinfo='percent+label',
                            hovertemplate='<b>%{label}</b><br>Value: $%{value:,.2f}<br>Percent: %{percent}<extra></extra>'
                        )
                        pie_fig.update_layout(
                            showlegend=True,
                            legend=dict(orientation="v", yanchor="middle", y=0.5),
                            margin=dict(l=20, r=20, t=40, b=20),
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='white'
                        )
                        st.plotly_chart(pie_fig, use_container_width=True)
                    
                    with col2:
                        # Colorful Bar Chart
                        bar_fig = px.bar(
                            x=labels,
                            y=values,
                            title="Position Values",
                            color=labels,
                            color_discrete_sequence=px.colors.qualitative.Set2
                        )
                        bar_fig.update_traces(
                            hovertemplate='<b>%{x}</b><br>Value: $%{y:,.2f}<extra></extra>',
                            texttemplate='$%{y:,.0f}',
                            textposition='outside'
                        )
                        bar_fig.update_layout(
                            showlegend=False,
                            margin=dict(l=20, r=20, t=40, b=20),
                            yaxis_title="Value ($)",
                            xaxis_title="Symbol",
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='white'
                        )
                        st.plotly_chart(bar_fig, use_container_width=True)
                    
                    # Performance Summary
                    st.markdown("### 📈 Performance Summary")
                    # Limit to maximum 6 columns to prevent layout issues
                    max_cols = min(len(labels), 6)
                    if max_cols > 0:
                        perf_cols = st.columns(max_cols)
                        
                        for i, (symbol, value) in enumerate(zip(labels[:max_cols], values[:max_cols])):
                            with perf_cols[i]:
                                pct = (value / sum(values) * 100) if sum(values) > 0 else 0
                                st.metric(
                                    label=symbol,
                                    value=f"${value:,.2f}",
                                    delta=f"{pct:.1f}% of portfolio"
                                )
                        
                        if len(labels) > 6:
                            st.info(f"Showing top {max_cols} positions. Total positions: {len(labels)}")
                else:
                    st.info("Add some stocks to see colorful charts!")
            else:
                st.info("No stocks in this portfolio yet.")
    st.markdown("</div>", unsafe_allow_html=True)

# ----- Trade Tab -----
with tab_trade:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("Trade")

    if not pm.portfolios:
        st.info("Create a portfolio first.")
    else:
        colL, colR = st.columns(2)

        with colL:
            st.markdown("#### Buy")
            pname_b = st.selectbox("Portfolio", options=list(pm.portfolios.keys()), key="buy_port")
            sym_b = st.text_input("Symbol", key="buy_sym")
            qty_b = st.number_input("Quantity", min_value=1, value=1, step=1, key="buy_qty")
            price_b = st.number_input("Price per share", min_value=0.0, value=100.0, step=0.01, key="buy_price")
            if st.button("Execute Buy", type="primary"):
                tx = Transaction(sym_b.strip().upper(), 'buy', int(qty_b), float(price_b))
                pm.process_transaction(pname_b, tx)
                p = pm.get_portfolio(pname_b)
                if p:
                    database.save_portfolio(p, st.session_state.username)
                st.success(f"Bought {qty_b} of {sym_b} @ ${price_b:.2f} in {pname_b}")

        with colR:
            st.markdown("#### Sell")
            pname_s = st.selectbox("Portfolio", options=list(pm.portfolios.keys()), key="sell_port")
            sym_s = st.text_input("Symbol", key="sell_sym")
            qty_s = st.number_input("Quantity", min_value=1, value=1, step=1, key="sell_qty")
            price_s = st.number_input("Price per share", min_value=0.0, value=100.0, step=0.01, key="sell_price")
            if st.button("Execute Sell"):
                tx = Transaction(sym_s.strip().upper(), 'sell', int(qty_s), float(price_s))
                pm.process_transaction(pname_s, tx)
                p = pm.get_portfolio(pname_s)
                if p:
                    database.save_portfolio(p, st.session_state.username)
                st.warning(f"Sold {qty_s} of {sym_s} @ ${price_s:.2f} from {pname_s}")

    st.markdown("</div>", unsafe_allow_html=True)

# ----- Live Market Tab -----
with tab_live:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("Live Market")

    sym_input = st.text_input("Symbols (comma separated)", value="AAPL, MSFT, TSLA", key="live_syms")
    colA, colB, colC = st.columns(3)
    with colA:
        period = st.selectbox("Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"], index=2)
    with colB:
        interval = st.selectbox("Interval", ["1m", "5m", "15m", "30m", "1h", "1d"], index=5)
    with colC:
        go_btn = st.button("Load Charts", type="primary")

    if go_btn and sym_input.strip():
        try:
            with st.spinner("Fetching market data..."):
                tickers = [s.strip().upper() for s in sym_input.split(",") if s.strip()]
                
                # Enhanced error handling for data fetching
                if len(tickers) == 1:
                    data = yf.download(tickers[0], period=period, interval=interval, auto_adjust=True, progress=False)
                    if not data.empty:
                        data = {tickers[0]: data}
                else:
                    data = yf.download(tickers=tickers, period=period, interval=interval, group_by='ticker', auto_adjust=True, threads=True, progress=False)

            # Build long-form for plotting
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
                import pandas as pd
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
                import plotly.graph_objects as go
                
                fig = go.Figure()
                
                # TradingView color scheme for different symbols
                tv_colors = ['#2962ff', '#ff6d00', '#00c853', '#e91e63', '#9c27b0']
                
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
                        text="Market Prices",
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

                # Quick trade panel
                st.markdown("### Quick Trade at Market Price")
                if pm.portfolios:
                    tcol1, tcol2, tcol3, tcol4, tcol5 = st.columns([1,1,1,1,2])
                    with tcol1:
                        q_port = st.selectbox("Portfolio", options=list(pm.portfolios.keys()), key="live_port")
                    with tcol2:
                        q_sym = st.selectbox("Symbol", options=list(latest_prices.keys()), key="live_sym")
                    with tcol3:
                        q_qty = st.number_input("Qty", min_value=1, value=1, step=1, key="live_qty")
                    with tcol4:
                        st.write("Price")
                        st.metric(label="", value=f"${latest_prices.get(q_sym, 0):,.2f}")
                    with tcol5:
                        c1, c2 = st.columns(2)
                        if c1.button("Buy", key="live_buy"):
                            tx = Transaction(q_sym, 'buy', int(q_qty), float(latest_prices[q_sym]))
                            pm.process_transaction(q_port, tx)
                            p = pm.get_portfolio(q_port)
                            if p:
                                database.save_portfolio(p, st.session_state.username)
                            st.success(f"Bought {q_qty} {q_sym} @ ${latest_prices[q_sym]:.2f}")
                        if c2.button("Sell", key="live_sell"):
                            tx = Transaction(q_sym, 'sell', int(q_qty), float(latest_prices[q_sym]))
                            pm.process_transaction(q_port, tx)
                            p = pm.get_portfolio(q_port)
                            if p:
                                database.save_portfolio(p, st.session_state.username)
                            st.warning(f"Sold {q_qty} {q_sym} @ ${latest_prices[q_sym]:.2f}")
                else:
                    st.info("Create a portfolio to trade.")
        except Exception as e:
            st.error(f"Failed to load market data: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# ----- Reports Tab -----
with tab_report:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("Reports")

    if not pm.portfolios:
        st.info("Create a portfolio first.")
    else:
        pname_r = st.selectbox("Portfolio", options=list(pm.portfolios.keys()), key="rep_port")
        if st.button("Generate Report", type="primary"):
            report_text = reporter.generate_portfolio_report(pname_r)
            st.code(report_text, language="markdown")
            st.download_button(
                label="Download Report",
                data=report_text,
                file_name=f"{pname_r}_report.txt",
                mime="text/plain",
            )

    st.markdown("</div>", unsafe_allow_html=True)

# ----- About Tab -----
with tab_about:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown(
        """
        ### About
        - **Purpose**: Track portfolios, positions and simple reports.
        - **Tech**: Streamlit UI, Python backend classes (`portfolio.py`, `transaction.py`, `report.py`, `database.py`).
        - **Prices**: `utils.fetch_stock_price()` uses random demo prices. Swap with a real API for live quotes.
        
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)
