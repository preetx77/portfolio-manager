# main.py

from portfolio import PortfolioManager
from transaction import Transaction
from report import ReportGenerator
import database

def print_menu():
    print("\nStock Portfolio Tracker Menu:")
    print("1. View Portfolios")
    print("2. Add Portfolio")
    print("3. Add Stock to Portfolio")
    print("4. Buy Stock")
    print("5. Sell Stock")
    print("6. Generate Portfolio Report")
    print("7. Exit")

def main():
    # Initialize database
    database.init_database()

    # Initialize portfolio manager and load portfolios from database
    portfolio_manager = PortfolioManager()
    portfolio_manager.load_portfolios()

    report_generator = ReportGenerator(portfolio_manager)

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            portfolio_manager.print_portfolios()

        elif choice == '2':
            portfolio_name = input("Enter portfolio name: ")
            portfolio_manager.add_portfolio(portfolio_name)
            database.save_portfolio(portfolio_manager.get_portfolio(portfolio_name))

        elif choice == '3':
            portfolio_name = input("Enter portfolio name: ")
            stock_symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            portfolio_manager.add_stock_to_portfolio(portfolio_name, stock_symbol, quantity)
            database.save_portfolio(portfolio_manager.get_portfolio(portfolio_name))

        elif choice == '4':
            portfolio_name = input("Enter portfolio name: ")
            stock_symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price per share: "))
            transaction = Transaction(stock_symbol, 'buy', quantity, price)
            portfolio_manager.process_transaction(portfolio_name, transaction)
            database.save_portfolio(portfolio_manager.get_portfolio(portfolio_name))
#F2
        elif choice == '5':
            portfolio_name = input("Enter portfolio name: ")
            stock_symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price per share: "))
            transaction = Transaction(stock_symbol, 'sell', quantity, price)
            portfolio_manager.process_transaction(portfolio_name, transaction)
            database.save_portfolio(portfolio_manager.get_portfolio(portfolio_name))

        elif choice == '6':
            portfolio_name = input("Enter portfolio name: ")
            report = report_generator.generate_portfolio_report(portfolio_name)
            print(report)

        elif choice == '7':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
