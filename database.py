# database.py
import sqlite3
from portfolio import Portfolio
from stock import Stock

DB_FILE = 'portfolio.db'

def init_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Detect legacy single-column portfolios table and migrate
    try:
        cursor.execute("PRAGMA table_info(portfolios)")
        cols = cursor.fetchall()
        # Legacy table had 1 column named 'name'
        if cols and len(cols) == 1 and cols[0][1].lower() == 'name':
            # read existing names
            cursor.execute('SELECT name FROM portfolios')
            legacy_rows = [r[0] for r in cursor.fetchall()]
            # rename legacy table
            cursor.execute('ALTER TABLE portfolios RENAME TO portfolios_legacy')
            conn.commit()
            # new tables will be created below, then we will import legacy data into default user
    except Exception:
        pass

    # Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE
        )
    ''')

    # Portfolios per user
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            UNIQUE(user_id, name),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # Holdings per portfolio
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()

    # If legacy table was renamed, import its data into default user portfolios
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='portfolios_legacy'")
        if cursor.fetchone():
            # Ensure default user exists
            cursor.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', ('default',))
            cursor.execute('SELECT id FROM users WHERE username = ?', ('default',))
            default_id = cursor.fetchone()[0]
            # Create portfolios for default user
            cursor.execute('SELECT name FROM portfolios_legacy')
            for (pname,) in cursor.fetchall():
                cursor.execute('INSERT OR IGNORE INTO portfolios (user_id, name) VALUES (?, ?)', (default_id, pname))
            # Drop legacy table
            cursor.execute('DROP TABLE portfolios_legacy')
            conn.commit()
    except Exception:
        # If anything goes wrong, ignore to avoid blocking app startup
        pass

    conn.close()

def _get_or_create_user_id(conn, username: str) -> int:
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (username,))
    cur.execute('SELECT id FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    return row[0]

def save_portfolio(portfolio: Portfolio, username: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    user_id = _get_or_create_user_id(conn, username)

    # Upsert portfolio
    cursor.execute('INSERT OR IGNORE INTO portfolios (user_id, name) VALUES (?, ?)', (user_id, portfolio.name))
    cursor.execute('SELECT id FROM portfolios WHERE user_id = ? AND name = ?', (user_id, portfolio.name))
    row = cursor.fetchone()
    if not row:
        conn.commit()
        conn.close()
        return
    portfolio_id = row[0]

    # Replace holdings for this portfolio
    cursor.execute('DELETE FROM holdings WHERE portfolio_id = ?', (portfolio_id,))
    for sym, data in portfolio.stocks.items():
        stock: Stock = data['stock']
        qty = data['quantity']
        cursor.execute(
            'INSERT INTO holdings (portfolio_id, symbol, quantity, price) VALUES (?, ?, ?, ?)',
            (portfolio_id, stock.symbol, qty, float(stock.price))
        )

    conn.commit()
    conn.close()

def load_portfolios(username: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # get user id (create if missing)
    user_id = _get_or_create_user_id(conn, username)

    # fetch portfolios
    cursor.execute('SELECT id, name FROM portfolios WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()

    portfolios = []
    for pid, name in rows:
        p = Portfolio(name)
        # fetch holdings
        cursor.execute('SELECT symbol, quantity, price FROM holdings WHERE portfolio_id = ?', (pid,))
        for sym, qty, price in cursor.fetchall():
            stock = Stock(sym, "Saved Stock", float(price))
            p.add_stock(stock, int(qty))
        portfolios.append(p)

    conn.close()
    return portfolios

def get_all_users():
    """Get list of all existing usernames"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT username FROM users ORDER BY username')
    users = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return users if users else ["default"]
