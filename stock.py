# stock.py

class Stock:
    def __init__(self, symbol, name, price):
        self.symbol = symbol
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.symbol}: {self.name} - ${self.price}"
