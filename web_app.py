"""
Portfolio Manager Web Application using FastAPI
Converts the Streamlit portfolio application to run on localhost
"""
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

# Import the existing portfolio management logic
from portfolio import PortfolioManager
from transaction import Transaction
from report import ReportGenerator
import database
import yfinance as yf
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go

# Create FastAPI application
app = FastAPI(title="Portfolio Manager", description="Advanced Portfolio Management Platform")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Global state
portfolio_manager = None
report_generator = None
current_user = "default"

def init_app():
    """Initialize the application and load data"""
    global portfolio_manager, report_generator

    # Initialize database
    database.init_database()

    # Initialize portfolio manager
    portfolio_manager = PortfolioManager()
    portfolio_manager.set_user(current_user)
    portfolio_manager.load_portfolios(current_user)

    report_generator = ReportGenerator(portfolio_manager)

    return portfolio_manager, report_generator

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main dashboard/home page"""
    global portfolio_manager, report_generator

    if portfolio_manager is None:
        portfolio_manager, report_generator = init_app()

    # Get portfolio statistics
    total_portfolios = len(portfolio_manager.portfolios)
    total_positions = sum(len(p.stocks) for p in portfolio_manager.portfolios.values())
    total_value = sum(p.calculate_portfolio_value() for p in portfolio_manager.portfolios.values())

    # Get market data
    market_data = get_market_data()

    # Get portfolio data for charts
    portfolio_data = []
    all_stocks_data = []

    for portfolio_name, portfolio in portfolio_manager.portfolios.items():
        portfolio_value = portfolio.calculate_portfolio_value()
        positions = len(portfolio.stocks)
        portfolio_data.append({
            'name': portfolio_name,
            'value': portfolio_value,
            'positions': positions
        })

        for symbol, stock_data in portfolio.stocks.items():
            stock = stock_data['stock']
            quantity = stock_data['quantity']
            if stock.symbol and stock.symbol.strip():
                value = stock.price * quantity
                all_stocks_data.append({
                    'portfolio': portfolio_name,
                    'symbol': stock.symbol.upper(),
                    'quantity': quantity,
                    'price': stock.price,
                    'value': value,
                    'name': stock.name
                })

    # Generate charts
    charts = generate_charts(portfolio_data, all_stocks_data)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_portfolios": total_portfolios,
        "total_positions": total_positions,
        "total_value": total_value,
        "current_user": current_user,
        "portfolio_data": portfolio_data,
        "market_data": market_data,
        "charts": charts
    })

@app.get("/portfolios", response_class=HTMLResponse)
async def portfolios(request: Request):
    """Portfolios management page"""
    if portfolio_manager is None:
        portfolio_manager, report_generator = init_app()

    portfolios_data = []
    for name, portfolio in portfolio_manager.portfolios.items():
        portfolios_data.append({
            'name': name,
            'value': portfolio.calculate_portfolio_value(),
            'stocks_count': len(portfolio.stocks),
            'stocks': [{'symbol': s.symbol, 'name': s.name, 'quantity': qty, 'price': s.price, 'value': s.price * qty}
                      for (symbol, data) in portfolio.stocks.items()
                      for (s, qty) in [(data['stock'], data['quantity'])] if s.symbol and s.symbol.strip()]
        })

    return templates.TemplateResponse("portfolios.html", {
        "request": request,
        "portfolios": portfolios_data,
        "current_user": current_user
    })

@app.post("/add_portfolio")
async def add_portfolio(request: Request, name: str = Form(...)):
    """Add a new portfolio"""
    if not name.strip():
        raise HTTPException(status_code=400, detail="Portfolio name is required")

    if portfolio_manager is None:
        portfolio_manager, report_generator = init_app()

    portfolio_manager.add_portfolio(name.strip())
    portfolio = portfolio_manager.get_portfolio(name.strip())
    if portfolio:
        database.save_portfolio(portfolio, current_user)

    return RedirectResponse(url="/portfolios", status_code=303)

@app.post("/add_stock")
async def add_stock(
    request: Request,
    portfolio_name: str = Form(...),
    symbol: str = Form(...),
    quantity: int = Form(...)
):
    """Add stock to portfolio"""
    if portfolio_manager is None:
        portfolio_manager, report_generator = init_app()

    portfolio_manager.add_stock_to_portfolio(portfolio_name, symbol.strip().upper(), quantity)
    portfolio = portfolio_manager.get_portfolio(portfolio_name)
    if portfolio:
        database.save_portfolio(portfolio, current_user)

    return RedirectResponse(url="/portfolios", status_code=303)

def get_market_data():
    """Get current market data for major indices"""
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
                    'current': float(current),
                    'change': float(change),
                    'change_pct': float(change_pct)
                }
        except:
            continue

    return market_data

def generate_charts(portfolio_data, all_stocks_data):
    """Generate charts for the dashboard"""
    charts = {}

    if portfolio_data:
        # Portfolio value comparison chart
        df = pd.DataFrame(portfolio_data)
        fig_bar = px.bar(
            df,
            x='name',
            y='value',
            title="Portfolio Values Comparison",
            color='value',
            color_continuous_scale='viridis'
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False
        )
        charts['portfolio_values'] = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)

        # Portfolio positions pie chart
        fig_pie = px.pie(
            df,
            values='positions',
            names='name',
            title="Portfolio Distribution by Positions"
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        charts['portfolio_positions'] = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)

    if all_stocks_data:
        df_stocks = pd.DataFrame(all_stocks_data)

        # Top holdings chart
        stock_totals = df_stocks.groupby('symbol')['value'].sum().reset_index()
        stock_totals = stock_totals.sort_values('value', ascending=False).head(10)

        fig_holdings = px.bar(
            stock_totals,
            x='symbol',
            y='value',
            title="Top 10 Holdings by Value",
            color='value',
            color_continuous_scale='viridis'
        )
        fig_holdings.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False
        )
        charts['top_holdings'] = json.dumps(fig_holdings, cls=plotly.utils.PlotlyJSONEncoder)

    return charts

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
