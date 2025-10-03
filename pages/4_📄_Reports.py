# pages/4_📄_Reports.py
import streamlit as st
from portfolio import PortfolioManager
from report import ReportGenerator
import database

# ---------- Page Config ----------
st.set_page_config(
    page_title="Portfolio Reports",
    page_icon="📄",
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
    st.session_state.reporter = ReportGenerator(pm)
    st.session_state.username = "default"

pm: PortfolioManager = st.session_state.pm
reporter: ReportGenerator = st.session_state.reporter

# ---------- Header ----------
st.markdown("<h1 class='title'>📄 Portfolio Reports</h1>", unsafe_allow_html=True)
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

# ---------- Reports Content ----------
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.subheader("Generate Portfolio Reports")

if not pm.portfolios:
    st.info("Create a portfolio first to generate reports.")
else:
    # Report Generation Interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        pname_r = st.selectbox("Select Portfolio", options=list(pm.portfolios.keys()), key="rep_port")
        
        # Report Options
        st.markdown("### 📋 Report Options")
        report_type = st.radio(
            "Report Type",
            ["📊 Standard Report", "📈 Detailed Analysis", "💼 Executive Summary"],
            key="report_type"
        )
        
        include_charts = st.checkbox("Include Charts", value=True)
        include_recommendations = st.checkbox("Include AI Recommendations", value=True)
        
    with col2:
        st.markdown("### 📊 Portfolio Preview")
        if pname_r:
            portfolio = pm.get_portfolio(pname_r)
            if portfolio:
                total_value = portfolio.calculate_portfolio_value()
                num_positions = len(portfolio.stocks)
                
                st.metric("Total Value", f"${total_value:,.2f}")
                st.metric("Positions", num_positions)
                
                if portfolio.stocks:
                    top_holding = max(portfolio.stocks.items(), 
                                    key=lambda x: x[1]['stock'].price * x[1]['quantity'])
                    st.metric("Top Holding", top_holding[0])

    # Generate Report Button
    if st.button("🚀 Generate Report", type="primary", use_container_width=True):
        with st.spinner("Generating comprehensive report..."):
            report_text = reporter.generate_portfolio_report(pname_r)
            
            # Display the report
            st.markdown("---")
            st.markdown("### 📄 Generated Report")
            
            # Enhanced report display
            st.markdown("<div class='glass' style='padding: 25px;'>", unsafe_allow_html=True)
            
            # Report header
            st.markdown(f"""
            <div style='text-align: center; margin-bottom: 30px;'>
                <h2 class='title'>Portfolio Report: {pname_r}</h2>
                <p style='color: #94a3b8;'>Generated on {st.session_state.get('username', 'default')} profile</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display report content
            st.code(report_text, language="markdown")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Download options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="📥 Download as TXT",
                    data=report_text,
                    file_name=f"{pname_r}_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                # Convert to markdown format
                markdown_report = f"# Portfolio Report: {pname_r}\n\n{report_text}"
                st.download_button(
                    label="📝 Download as MD",
                    data=markdown_report,
                    file_name=f"{pname_r}_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col3:
                if st.button("📧 Email Report", use_container_width=True):
                    st.info("📧 Email functionality would be implemented here")

st.markdown("</div>", unsafe_allow_html=True)

# Report Templates Section
st.write("")
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("### 📋 Report Templates")

template_col1, template_col2, template_col3 = st.columns(3)

with template_col1:
    st.markdown("""
    <div class='glass' style='padding: 20px; text-align: center; height: 200px;'>
        <div style='font-size: 3rem; margin-bottom: 15px;'>📊</div>
        <h4 style='color: #22d3ee; margin-bottom: 10px;'>Standard Report</h4>
        <p style='color: #94a3b8; font-size: 0.9rem;'>
            Basic portfolio overview with holdings, values, and simple metrics
        </p>
    </div>
    """, unsafe_allow_html=True)

with template_col2:
    st.markdown("""
    <div class='glass' style='padding: 20px; text-align: center; height: 200px;'>
        <div style='font-size: 3rem; margin-bottom: 15px;'>📈</div>
        <h4 style='color: #a78bfa; margin-bottom: 10px;'>Detailed Analysis</h4>
        <p style='color: #94a3b8; font-size: 0.9rem;'>
            Comprehensive analysis with performance metrics and risk assessment
        </p>
    </div>
    """, unsafe_allow_html=True)

with template_col3:
    st.markdown("""
    <div class='glass' style='padding: 20px; text-align: center; height: 200px;'>
        <div style='font-size: 3rem; margin-bottom: 15px;'>💼</div>
        <h4 style='color: #34d399; margin-bottom: 10px;'>Executive Summary</h4>
        <p style='color: #94a3b8; font-size: 0.9rem;'>
            High-level overview perfect for stakeholders and decision makers
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Report History Section
st.write("")
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("### 📚 Report Features")

features = [
    "📊 **Portfolio Valuation**: Complete breakdown of all holdings and their current market values",
    "📈 **Performance Metrics**: Track gains, losses, and percentage changes over time",
    "🎯 **Asset Allocation**: Visual representation of portfolio diversification",
    "⚠️ **Risk Analysis**: Identify concentration risks and suggest improvements",
    "💡 **AI Recommendations**: Smart insights based on market trends and portfolio composition",
    "📅 **Historical Tracking**: Compare current performance with previous periods",
    "🔄 **Rebalancing Suggestions**: Optimize portfolio allocation for better returns",
    "📱 **Export Options**: Download reports in multiple formats (TXT, MD, PDF)"
]

for feature in features:
    st.markdown(f"- {feature}")

st.markdown("</div>", unsafe_allow_html=True)

# Quick Navigation
st.write("")
st.markdown("<div class='glass' style='text-align: center; padding: 20px;'>", unsafe_allow_html=True)
st.markdown("### 🚀 Quick Actions")

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    if st.button("📊 View Portfolios", use_container_width=True):
        st.switch_page("pages/1_📊_Portfolios.py")

with nav_col2:
    if st.button("💹 Start Trading", use_container_width=True):
        st.switch_page("pages/2_💹_Trading.py")

with nav_col3:
    if st.button("📈 Live Market", use_container_width=True):
        st.switch_page("pages/3_📈_Live_Market.py")

st.markdown("</div>", unsafe_allow_html=True)
