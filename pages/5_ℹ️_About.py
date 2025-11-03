# pages/5_ℹ️_About.py
import streamlit as st

# ---------- Page Config ----------
st.set_page_config(
    page_title="About Portfolio Tracker",
    page_icon="ℹ️",
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

# ---------- Header ----------
st.markdown("<h1 class='title'>ℹ️ About Portfolio Tracker</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------- Sidebar Navigation ----------
st.sidebar.header("🚀 Navigation")
with st.sidebar:
    st.page_link("home.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/1_📊_Portfolios.py", label="📊 Portfolios", icon="📊")
    st.page_link("pages/2_💹_Trading.py", label="💹 Trading", icon="💹")
    st.page_link("pages/3_📈_Live_Market.py", label="📈 Live Market", icon="📈")
    st.page_link("pages/6_📊_Charts.py", label="📊 Charts", icon="📊")
    st.page_link("pages/4_📄_Reports.py", label="📄 Reports", icon="📄")
    st.page_link("pages/5_ℹ️_About.py", label="ℹ️ About", icon="ℹ️")

# ---------- About Content ----------

# Hero Section
st.markdown("""
<div class='glass' style='text-align: center; padding: 40px 20px; margin-bottom: 30px;'>
    <h2 class='title' style='font-size: 2.5rem; margin-bottom: 20px;'>
        🚀 Advanced Portfolio Management Platform
    </h2>
    <p style='font-size: 1.2rem; color: #94a3b8; line-height: 1.6;'>
        A cutting-edge financial technology solution built with modern web technologies
        and designed for the future of portfolio management.
    </p>
</div>
""", unsafe_allow_html=True)

# Main Features
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("### 🎯 **Purpose & Vision**")
    st.markdown("""
    **Portfolio Tracker** is designed to democratize advanced portfolio management tools, 
    making sophisticated financial analytics accessible to everyone. Our platform combines 
    real-time market data, AI-powered insights, and intuitive design to help users make 
    informed investment decisions.
    
    **Key Objectives:**
    - 📊 Simplify complex financial data
    - 🚀 Provide real-time market insights  
    - 🎨 Deliver a beautiful, modern user experience
    - 🔒 Ensure data security and privacy
    - 📱 Enable cross-platform accessibility
    """)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("### 🛠️ **Technology Stack**")
    st.markdown("""
    Built with cutting-edge technologies for optimal performance and scalability:
    
    **Frontend & UI:**
    - 🎨 **Streamlit** - Modern web app framework
    - 🌈 **Custom CSS** - Futuristic glassmorphism design
    - 📊 **Plotly** - Interactive data visualizations
    
    **Backend & Data:**
    - 🐍 **Python** - Core application logic
    - 💾 **SQLite** - Lightweight database storage
    - 📡 **yfinance** - Real-time market data API
    
    **Architecture:**
    - 🏗️ **Multi-page Application** - Organized page structure
    - 🔄 **Session Management** - Persistent user state
    - 📱 **Responsive Design** - Works on all devices
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Features Overview
st.write("")
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("### 🌟 **Platform Features**")

feature_col1, feature_col2, feature_col3, feature_col4 = st.columns(4)

with feature_col1:
    st.markdown("""
    **📊 Portfolio Management**
    - Multi-portfolio tracking
    - Real-time valuations
    - Interactive charts
    - Performance analytics
    - Asset allocation views
    """)

with feature_col2:
    st.markdown("""
    **💹 Trading Platform**
    - Buy/sell order execution
    - Market price trading
    - Transaction history
    - Portfolio rebalancing
    - Risk management tools
    """)

with feature_col3:
    st.markdown("""
    **📈 Live Market Data**
    - Real-time price feeds
    - TradingView-style charts
    - Multiple timeframes
    - Market statistics
    - Technical indicators
    """)

with feature_col4:
    st.markdown("""
    **📄 Smart Reports**
    - Automated generation
    - Multiple formats
    - AI-powered insights
    - Performance analysis
    - Export capabilities
    """)

st.markdown("</div>", unsafe_allow_html=True)

# Technical Details
st.write("")
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("### ⚙️ **Technical Architecture**")

arch_col1, arch_col2 = st.columns(2)

with arch_col1:
    st.markdown("""
    **🏗️ Application Structure:**
    ```
    portfolio-manager/
    ├── home.py                 # Main landing page
    ├── pages/                  # Multi-page structure
    │   ├── 1_📊_Portfolios.py  # Portfolio management
    │   ├── 2_💹_Trading.py     # Trading interface
    │   ├── 3_📈_Live_Market.py # Market data
    │   ├── 4_📄_Reports.py     # Report generation
    │   └── 5_ℹ️_About.py       # About page
    ├── portfolio.py            # Core portfolio logic
    ├── transaction.py          # Transaction handling
    ├── report.py              # Report generation
    ├── database.py            # Data persistence
    └── utils.py               # Utility functions
    ```
    """)

with arch_col2:
    st.markdown("""
    **🔧 Key Components:**
    
    - **PortfolioManager**: Core business logic for managing multiple portfolios
    - **Transaction**: Handles buy/sell operations with validation
    - **ReportGenerator**: Creates comprehensive portfolio reports
    - **Database**: SQLite-based persistence layer
    - **Multi-page Navigation**: Streamlit's native page routing
    - **Session State**: Maintains user data across pages
    - **Real-time Data**: Integration with financial APIs
    - **Responsive UI**: Glassmorphism design system
    """)

st.markdown("</div>", unsafe_allow_html=True)

# Usage Guide
st.write("")
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("### 📚 **Getting Started**")

guide_col1, guide_col2 = st.columns(2)

with guide_col1:
    st.markdown("""
    **🚀 Quick Start Guide:**
    
    1. **🏠 Home Page**: Overview of your portfolio ecosystem
    2. **👤 Profile Setup**: Create or switch between user profiles
    3. **📊 Create Portfolio**: Add your first investment portfolio
    4. **📈 Add Stocks**: Populate portfolios with stock positions
    5. **💹 Execute Trades**: Buy and sell stocks at market prices
    6. **📊 Monitor Performance**: Track real-time portfolio values
    7. **📄 Generate Reports**: Create detailed analysis reports
    """)

with guide_col2:
    st.markdown("""
    **💡 Pro Tips:**
    
    - **Diversification**: Spread investments across different sectors
    - **Regular Monitoring**: Check portfolio performance regularly
    - **Market Analysis**: Use live market data for informed decisions
    - **Risk Management**: Never invest more than you can afford to lose
    - **Report Analysis**: Review generated reports for insights
    - **Profile Management**: Use multiple profiles for different strategies
    - **Data Export**: Download reports for external analysis
    """)

st.markdown("</div>", unsafe_allow_html=True)

# Version & Credits
st.write("")
version_col1, version_col2 = st.columns(2)

with version_col1:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("""
    ### 📋 **Version Information**
    
    - **Version**: 2.0.0 (Multi-page Edition)
    - **Release Date**: October 2025
    - **Architecture**: Multi-page Streamlit Application
    - **Database**: SQLite with persistent storage
    - **API Integration**: yfinance for real-time data
    - **UI Framework**: Custom glassmorphism design
    - **Compatibility**: Cross-platform (Windows, macOS, Linux)
    """)
    st.markdown("</div>", unsafe_allow_html=True)

with version_col2:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("""
    ### 🙏 **Acknowledgments**
    
    **Built with:**
    - 🎨 **Streamlit** - Web application framework
    - 📊 **Plotly** - Interactive visualizations  
    - 📡 **yfinance** - Financial data API
    - 🐍 **Python** - Core programming language
    - 💾 **SQLite** - Database management
    
    **Special Thanks:**
    - Open source community for amazing tools
    - Financial data providers for market access
    - Design inspiration from modern fintech apps
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.write("")
st.markdown("""
<div class='glass' style='text-align: center; padding: 25px;'>
    <h4 style='color: #94a3b8; margin-bottom: 20px;'>🚀 Ready to Start Your Investment Journey?</h4>
    <p style='color: #94a3b8; margin-bottom: 20px;'>
        Join thousands of users who trust Portfolio Tracker for their investment management needs.
    </p>
</div>
""", unsafe_allow_html=True)

# Quick Navigation
st.write("")
st.markdown("<div class='glass' style='text-align: center; padding: 20px;'>", unsafe_allow_html=True)
st.markdown("### 🚀 Quick Actions")

nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

with nav_col1:
    if st.button("🏠 Go Home", use_container_width=True):
        st.switch_page("home.py")

with nav_col2:
    if st.button("📊 View Portfolios", use_container_width=True):
        st.switch_page("pages/1_📊_Portfolios.py")

with nav_col3:
    if st.button("💹 Start Trading", use_container_width=True):
        st.switch_page("pages/2_💹_Trading.py")

with nav_col4:
    if st.button("📈 Live Market", use_container_width=True):
        st.switch_page("pages/3_📈_Live_Market.py")

st.markdown("</div>", unsafe_allow_html=True)
