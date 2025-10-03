# 🚀 Advanced Portfolio Tracker

<div align="center">

![Portfolio Tracker](https://img.shields.io/badge/Portfolio-Tracker-blue?style=for-the-badge&logo=chart-line)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A cutting-edge web-based portfolio management platform with real-time analytics, AI-powered insights, and futuristic design.**

[🌟 Features](#-features) • [🚀 Quick Start](#-quick-start) • [📊 Screenshots](#-screenshots) • [🛠️ Tech Stack](#️-tech-stack)

</div>

---

## 🌟 Features

### 🏠 **Advanced Home Dashboard**
- **Real-time Market Overview** - Live S&P 500, Dow Jones, NASDAQ, and VIX data
- **Portfolio Distribution Charts** - Interactive pie charts, bar graphs, and heatmaps
- **Advanced Analytics** - Risk scoring, Sharpe ratio, and diversification metrics
- **Glassmorphism UI** - Modern, futuristic design with smooth animations

### 📊 **Portfolio Management**
- **Multi-portfolio Tracking** - Manage unlimited portfolios simultaneously
- **Interactive Visualizations** - Pie charts, bar graphs, and allocation analysis
- **Real-time Valuations** - Live portfolio value calculations
- **Performance Metrics** - Comprehensive analytics and insights

### 💹 **Trading Platform**
- **Instant Order Execution** - Buy and sell stocks with custom pricing
- **Market Price Trading** - Execute trades at live market prices
- **Transaction History** - Complete record of all trading activities
- **Portfolio Rebalancing** - Smart allocation suggestions

### 📈 **Live Market Data**
- **TradingView-style Charts** - Professional-grade market visualizations
- **Multiple Timeframes** - 1m to 1y intervals with various periods
- **Real-time Price Feeds** - Live stock price updates via yfinance API
- **Market Statistics** - Comprehensive market overview and analytics

### 📄 **Smart Reports**
- **AI-powered Insights** - Automated portfolio analysis and recommendations
- **Multiple Export Formats** - TXT, MD, and PDF report generation
- **Performance Analysis** - Detailed risk assessment and metrics
- **Custom Formatting** - Professional report layouts

### 👤 **Multi-user Support**
- **Profile Management** - Create and switch between user profiles
- **Data Persistence** - SQLite database for reliable data storage
- **Session Management** - Seamless user experience across pages

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/preetx77/portfolio-manager.git
   cd portfolio-manager
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install streamlit plotly yfinance pandas numpy
   ```

### Running the Application

**Start the web application:**
```bash
streamlit run home.py
```

**Access the application:**
- Open your browser and navigate to `http://localhost:8501`
- The application will automatically open in your default browser

## 📱 Application Structure

### Multi-page Architecture
```
portfolio-manager/
├── home.py                     # 🏠 Main landing page with dashboard
├── pages/
│   ├── 1_📊_Portfolios.py     # Portfolio management interface
│   ├── 2_💹_Trading.py        # Trading platform
│   ├── 3_📈_Live_Market.py    # Real-time market data
│   ├── 4_📄_Reports.py        # Report generation
│   └── 5_ℹ️_About.py          # Platform information
├── portfolio.py                # Core portfolio logic
├── stock.py                   # Stock class definition
├── transaction.py             # Transaction handling
├── database.py                # SQLite data persistence
├── report.py                  # Report generation engine
├── utils.py                   # Utility functions
└── portfolio.db               # SQLite database (auto-created)
```

## 🛠️ Tech Stack

### Frontend & UI
- **🎨 Streamlit** - Modern web application framework
- **🌈 Custom CSS** - Futuristic glassmorphism design system
- **📊 Plotly** - Interactive data visualizations and charts

### Backend & Data
- **🐍 Python** - Core application logic and processing
- **💾 SQLite** - Lightweight, reliable database storage
- **📡 yfinance** - Real-time financial data API integration
- **🔢 Pandas/NumPy** - Advanced data analysis and manipulation

### Architecture
- **🏗️ Multi-page Application** - Organized, scalable page structure
- **🔄 Session Management** - Persistent user state across pages
- **📱 Responsive Design** - Works seamlessly on all devices
- **⚡ Real-time Updates** - Live data integration and processing

## 📊 Key Features Breakdown

| Feature | Description | Technology |
|---------|-------------|------------|
| **Real-time Data** | Live market prices and indices | yfinance API |
| **Interactive Charts** | Professional trading visualizations | Plotly.js |
| **Multi-user Support** | Profile management system | SQLite + Session State |
| **Advanced Analytics** | Risk metrics and performance analysis | Pandas + NumPy |
| **Modern UI** | Glassmorphism design with animations | Custom CSS + Streamlit |
| **Report Generation** | Automated insights and exports | Python + AI algorithms |

## 🎯 Getting Started Guide

1. **🏠 Home Page** - Start with the dashboard overview
2. **👤 Create Profile** - Set up your user profile in the sidebar
3. **📊 Add Portfolio** - Create your first investment portfolio
4. **📈 Add Stocks** - Populate portfolios with stock positions
5. **💹 Execute Trades** - Buy and sell stocks at market prices
6. **📊 Monitor Performance** - Track real-time portfolio values
7. **📄 Generate Reports** - Create detailed analysis reports

## 💡 Pro Tips

- **Diversification**: Spread investments across different sectors and asset classes
- **Regular Monitoring**: Check portfolio performance regularly using the dashboard
- **Market Analysis**: Use live market data for informed investment decisions
- **Risk Management**: Never invest more than you can afford to lose
- **Report Analysis**: Review generated reports for actionable insights
- **Profile Management**: Use multiple profiles for different investment strategies

## 🔧 Advanced Configuration

### Environment Variables
```bash
# Optional: Set custom database path
export PORTFOLIO_DB_PATH="/path/to/custom/portfolio.db"

# Optional: Configure API settings
export YFINANCE_TIMEOUT=30
```

### Custom Styling
The application uses a custom glassmorphism theme. You can modify the CSS in each page file to customize the appearance.

## 📈 Performance & Scalability

- **Database**: SQLite handles thousands of portfolios and transactions efficiently
- **Real-time Data**: Optimized API calls with caching and error handling
- **Memory Usage**: Efficient data structures for large portfolio datasets
- **Response Time**: Sub-second page loads and chart rendering

## 🤝 Contributing

We welcome contributions! Here's how you can help improve the Portfolio Tracker:

### Development Setup
1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/portfolio-manager.git
   cd portfolio-manager
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Making Changes
1. **Make your changes** following the existing code style
2. **Test your changes** thoroughly
3. **Update documentation** if needed
4. **Commit your changes**:
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Create a Pull Request** on GitHub

### Code Style Guidelines
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Maintain the existing glassmorphism UI theme
- Test all new features thoroughly

## 🐛 Issues & Support

### Reporting Issues
If you encounter any problems:

1. **Check existing issues** on GitHub first
2. **Create a detailed issue** with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - System information (OS, Python version)

### Getting Help
- 📖 **Documentation**: Check this README and code comments
- 💬 **Discussions**: Use GitHub Discussions for questions
- 🐛 **Bug Reports**: Create an issue with the bug template
- 💡 **Feature Requests**: Create an issue with the feature template

## 🚀 Deployment

### Local Development
```bash
# Run in development mode
streamlit run home.py --server.runOnSave true
```

### Production Deployment

#### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with one click

#### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Heroku Deployment
1. Create `requirements.txt`:
   ```
   streamlit
   plotly
   yfinance
   pandas
   numpy
   ```
2. Create `Procfile`:
   ```
   web: sh setup.sh && streamlit run home.py
   ```
3. Deploy to Heroku

## 📊 Roadmap

### Upcoming Features
- [ ] **Real-time Notifications** - Price alerts and portfolio updates
- [ ] **Advanced Charting** - Technical indicators and drawing tools
- [ ] **Social Features** - Share portfolios and follow other investors
- [ ] **Mobile App** - Native iOS and Android applications
- [ ] **API Integration** - RESTful API for external integrations
- [ ] **Machine Learning** - Predictive analytics and recommendations
- [ ] **Cryptocurrency Support** - Bitcoin, Ethereum, and altcoin tracking
- [ ] **Options Trading** - Options contracts and strategies

### Version History
- **v2.0.0** - Multi-page architecture with advanced analytics
- **v1.5.0** - Live market data integration
- **v1.0.0** - Initial web-based portfolio tracker

## 🏆 Acknowledgments

### Built With Love Using
- **Streamlit Team** - For the amazing web framework
- **Plotly** - For beautiful, interactive visualizations
- **yfinance** - For reliable financial data access
- **Python Community** - For the incredible ecosystem

### Special Thanks
- Contributors who helped improve the platform
- Beta testers who provided valuable feedback
- Open source community for inspiration and tools

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ **Commercial Use** - Use for commercial projects
- ✅ **Modification** - Modify and distribute
- ✅ **Distribution** - Share with others
- ✅ **Private Use** - Use privately
- ❌ **Liability** - No warranty provided
- ❌ **Warranty** - Use at your own risk

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

**Made with ❤️ by [preetx77](https://github.com/preetx77)**

**🚀 [Live Demo](https://portfolio-tracker-demo.streamlit.app) • 📖 [Documentation](https://github.com/preetx77/portfolio-manager/wiki) • 🐛 [Report Bug](https://github.com/preetx77/portfolio-manager/issues)**

</div>
