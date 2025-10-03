# pages/1_📊_Portfolios.py
import streamlit as st
from portfolio import PortfolioManager
from transaction import Transaction
from report import ReportGenerator
import database
import plotly.express as px

# ---------- Page Config ----------
st.set_page_config(
    page_title="Portfolio Management",
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
    .metric-card { text-align:center; padding: 10px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); }
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

# ---------- Header ----------
st.markdown("<h1 class='title'>📊 Portfolio Management</h1>", unsafe_allow_html=True)
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

# ---------- Portfolio Management Content ----------
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.subheader("Your Portfolios")

if not pm.portfolios:
    st.info("No portfolios yet. Use the sidebar to create one.")
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
                        margin=dict(l=20, r=20, t=40, b=20)
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
                        xaxis_title="Symbol"
                    )
                    st.plotly_chart(bar_fig, use_container_width=True)
                
                # Performance Summary
                st.markdown("### 📈 Performance Summary")
                perf_cols = st.columns(len(labels))
                
                for i, (symbol, value) in enumerate(zip(labels, values)):
                    with perf_cols[i]:
                        pct = (value / sum(values) * 100) if sum(values) > 0 else 0
                        st.metric(
                            label=symbol,
                            value=f"${value:,.2f}",
                            delta=f"{pct:.1f}% of portfolio"
                        )
            else:
                st.info("Add some stocks to see colorful charts!")
        else:
            st.info("No stocks in this portfolio yet.")
st.markdown("</div>", unsafe_allow_html=True)
