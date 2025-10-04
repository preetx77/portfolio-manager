# transaction.py

from stock import Stock

class Transaction:
    def __init__(self, symbol, action, quantity, price):
        self.symbol = symbol
        self.action = action  # 'buy' or 'sell'
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f"Transaction: {self.action} {self.quantity} shares of {self.symbol} at ${self.price} per share"

    def execute(self, portfolio):
        if self.action == 'buy':
            self.execute_buy(portfolio)
        elif self.action == 'sell':
            self.execute_sell(portfolio)

    def execute_buy(self, portfolio):
        stock = Stock(self.symbol, "Dummy Stock", self.price)
        portfolio.add_stock(stock, self.quantity)

    def execute_sell(self, portfolio):
        if portfolio.has_stock(self.symbol):
            current_quantity = portfolio.get_stock_quantity(self.symbol)
            if current_quantity >= self.quantity:
                stock = Stock(self.symbol, "Dummy Stock", self.price)
                portfolio.remove_stock(stock, self.quantity)
            else:
                raise ValueError(f"Not enough shares of {self.symbol} to sell. Available: {current_quantity}, Requested: {self.quantity}")
        else:
            raise ValueError(f"No shares of {self.symbol} in portfolio.")
