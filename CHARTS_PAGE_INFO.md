# 📊 Charts Page - Feature Documentation

## Overview
A new dedicated **Charts** page has been added to the Portfolio Manager application, providing advanced visualization and analytics capabilities.

## Location
- **File**: `pages/6_📊_Charts.py`
- **Navigation**: Available in the sidebar on all pages

## Features

### 1. **Price Chart** 📈
- Track price movements of multiple stocks simultaneously
- Real-time line charts with interactive tooltips
- Support for multiple symbols comparison
- TradingView-style color scheme

### 2. **Candlestick Chart** 🕯️
- OHLC (Open, High, Low, Close) data visualization
- Technical indicators:
  - SMA 20 (20-day Simple Moving Average)
  - SMA 50 (50-day Simple Moving Average)
- Best for detailed price action analysis
- Professional trading view

### 3. **Volume Chart** 📊
- Combined price and volume analysis
- Color-coded volume bars (green for up days, red for down days)
- Dual-pane view for better correlation analysis
- Identify volume patterns and trends

### 4. **Comparison Chart** 📊
- Normalized performance comparison
- Shows percentage change from starting point
- Perfect for comparing relative performance
- Supports multiple stocks simultaneously

### 5. **Portfolio Performance** 💼
- Track entire portfolio value over time
- Historical portfolio valuation
- Portfolio composition pie chart
- Real-time allocation analysis

## Configuration Options

### Time Periods
- 1 day (1d)
- 5 days (5d)
- 1 month (1mo)
- 3 months (3mo)
- 6 months (6mo)
- 1 year (1y)
- 2 years (2y)
- 5 years (5y)

### Intervals
- 1 minute (1m)
- 5 minutes (5m)
- 15 minutes (15m)
- 30 minutes (30m)
- 1 hour (1h)
- 1 day (1d)
- 1 week (1wk)
- 1 month (1mo)

## Stock Selection Modes

### From Portfolio
- Select any existing portfolio
- Choose stocks from your holdings
- Quick access to your investments

### Custom Symbols
- Enter any stock symbols (comma-separated)
- Example: AAPL, MSFT, GOOGL, TSLA
- Supports all Yahoo Finance tickers

## Technical Details

### Technologies Used
- **Streamlit**: Web framework
- **Plotly**: Interactive charting library
- **yfinance**: Real-time market data
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations

### Data Source
- Yahoo Finance API via yfinance
- Real-time and historical data
- Automatic data validation

### Validation
- Period/interval compatibility checking
- Prevents invalid data requests
- User-friendly error messages

## Usage Tips

1. **For Day Trading**: Use 1d period with 1m or 5m intervals
2. **For Swing Trading**: Use 1mo period with 1h or 1d intervals
3. **For Long-term Analysis**: Use 1y or longer with 1d or 1wk intervals
4. **Portfolio Tracking**: Use Portfolio Performance chart with 3mo or 6mo period

## Navigation Integration

The Charts page is now integrated into all navigation menus across the application:
- Home page
- Portfolios page
- Trading page
- Live Market page
- Reports page
- About page

## Quick Actions

From the Charts page, you can quickly navigate to:
- 📈 Live Market
- 📊 Portfolios
- 💹 Trading

## Future Enhancements (Potential)

- [ ] Add more technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Export charts as images
- [ ] Save favorite chart configurations
- [ ] Add drawing tools for technical analysis
- [ ] Real-time auto-refresh option
- [ ] Custom date range selection
- [ ] Compare portfolio vs benchmark indices

## Commit Information

- **Commit**: b671ffd
- **Message**: "Add dedicated Charts page with advanced visualization features"
- **Files Changed**: 6
- **Lines Added**: 519+

---

**Created**: November 3, 2025
**Version**: 1.0
