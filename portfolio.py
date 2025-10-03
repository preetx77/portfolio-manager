# portfolio.py

from stock import Stock

class Portfolio:
    def __init__(self, name):
        self.name = name
        self.stocks = {}

    def add_stock(self, stock, quantity):
        if stock.symbol in self.stocks:
            self.stocks[stock.symbol]['quantity'] += quantity
        else:
            self.stocks[stock.symbol] = {
                'stock': stock,
                'quantity': quantity
            }

    def remove_stock(self, stock, quantity):
        if stock.symbol in self.stocks:
            if self.stocks[stock.symbol]['quantity'] >= quantity:
                self.stocks[stock.symbol]['quantity'] -= quantity
                if self.stocks[stock.symbol]['quantity'] == 0:
                    del self.stocks[stock.symbol]

    def calculate_portfolio_value(self):
        total_value = 0.0
        for stock_data in self.stocks.values():
            stock = stock_data['stock']
            quantity = stock_data['quantity']
            total_value += stock.price * quantity
        return total_value

    def __str__(self):
        return f"Portfolio: {self.name}, Total Value: ${self.calculate_portfolio_value()}"

    def print_stocks(self):
        print(f"\nStocks in Portfolio '{self.name}':")
        for stock_data in self.stocks.values():
            print(f"{stock_data['stock']} - Quantity: {stock_data['quantity']}")

    def has_stock(self, symbol):
        return symbol in self.stocks

    def get_stock_quantity(self, symbol):
        if symbol in self.stocks:
            return self.stocks[symbol]['quantity']
        return 0

class PortfolioManager:
    def __init__(self):
        # name -> Portfolio
        self.portfolios = {}
        self.current_user = "default"

    def set_user(self, username: str):
        self.current_user = username or "default"

    def load_portfolios(self, username: str = None):
        import database
        user = username or self.current_user
        portfolios = database.load_portfolios(user)
        self.portfolios = {p.name: p for p in portfolios}

    def print_portfolios(self):
        if not self.portfolios:
            print("\nNo portfolios found. Use 'Add Portfolio' to create one.")
            return
        print("\nPortfolios:")
        for name, portfolio in self.portfolios.items():
            print(f"- {name}: Total Value ${portfolio.calculate_portfolio_value():.2f}")

    def add_portfolio(self, name):
        if name not in self.portfolios:
            self.portfolios[name] = Portfolio(name)
        else:
            print(f"Portfolio '{name}' already exists.")

    def get_portfolio(self, name):
        return self.portfolios.get(name)

    def add_stock_to_portfolio(self, portfolio_name, stock_symbol, quantity):
        from stock import Stock
        from utils import fetch_stock_price
        portfolio = self.get_portfolio(portfolio_name)
        if not portfolio:
            print(f"Portfolio '{portfolio_name}' does not exist.")
            return
        price = fetch_stock_price(stock_symbol)
        stock = Stock(stock_symbol, "Fetched Stock", price)
        portfolio.add_stock(stock, quantity)

    def process_transaction(self, portfolio_name, transaction):
        portfolio = self.get_portfolio(portfolio_name)
        if not portfolio:
            print(f"Portfolio '{portfolio_name}' does not exist.")
            return
        transaction.execute(portfolio)
