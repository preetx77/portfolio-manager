# Stock Portfolio Tracker

## Description

This is a command-line application for managing stock portfolios. It allows users to:

- Create and manage multiple portfolios.
- Add stocks to portfolios.
- Record stock purchases and sales.
- View portfolio performance.
- Generate portfolio reports.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
   (Replace `<repository-url>` with the actual URL of this repository)
2. Navigate to the project directory:
   ```bash
   cd <repository-directory-name>
   ```
3. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. No external Python libraries are strictly required for the basic functionality as it uses built-in libraries like `sqlite3`.

## Usage

To run the application, execute the `main.py` script from the project's root directory:

```bash
python3 main.py
```

You will be presented with a menu to interact with the portfolio tracker.

## Project Structure

- `main.py`: The main entry point of the application. Handles user interaction and orchestrates the different modules.
- `portfolio.py`: Defines the `Portfolio` and `PortfolioManager` classes. `Portfolio` manages a collection of stocks, and `PortfolioManager` manages multiple portfolios.
- `stock.py`: Defines the `Stock` class, representing a single stock.
- `transaction.py`: Defines the `Transaction` class for buying or selling stocks.
- `database.py`: Handles all database interactions (SQLite) for storing and retrieving portfolio data.
- `utils.py`: Contains utility functions (e.g., fetching stock prices - currently a placeholder).
- `report.py`: (Assumed, based on `main.py` import) Likely contains logic for generating portfolio reports.
- `portfolio.db`: The SQLite database file where data is stored (will be created on first run if it doesn't exist).

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix (`git checkout -b feature/your-feature-name` or `bugfix/issue-number`).
3. Make your changes.
4. Ensure your code adheres to any existing style guidelines.
5. Write or update tests for your changes.
6. Commit your changes (`git commit -am 'Add some feature'`).
7. Push to the branch (`git push origin your-branch-name`).
8. Create a new Pull Request against the `main` branch of the original repository.

## License

This project is licensed under the MIT License. (If a `LICENSE` file is present, it takes precedence. Otherwise, assume MIT).
