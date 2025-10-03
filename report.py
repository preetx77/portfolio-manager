# report.py

class ReportGenerator:
    def __init__(self, portfolio_manager):
        self.portfolio_manager = portfolio_manager

    def generate_portfolio_report(self, portfolio_name):
        portfolio = self.portfolio_manager.get_portfolio(portfolio_name)
        if not portfolio:
            return f"Portfolio '{portfolio_name}' does not exist."

        lines = []
        lines.append(f"Report for Portfolio: {portfolio.name}")
        lines.append("-")
        total_value = 0.0
        if not portfolio.stocks:
            lines.append("No stocks in this portfolio.")
        else:
            for symbol, data in portfolio.stocks.items():
                stock = data['stock']
                qty = data['quantity']
                value = stock.price * qty
                total_value += value
                lines.append(f"{symbol} | {stock.name} | Qty: {qty} | Price: ${stock.price:.2f} | Value: ${value:.2f}")
        lines.append("-")
        lines.append(f"Total Portfolio Value: ${total_value:.2f}")
        return "\n".join(lines)
