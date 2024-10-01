import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('fund_management.db', check_same_thread=False)
cursor = conn.cursor()

# Create the necessary tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,        -- Unique ID for each user (auto-increment)
        telegram_id INTEGER UNIQUE,         -- User's Telegram ID (unique)
        username TEXT UNIQUE,               -- Chosen username (unique)
        balance REAL DEFAULT 0.00,          -- User balance starts at 0.00
        chat_id INTEGER                     -- Group or chat ID the user belongs to
    )
''')
conn.commit()

def add_user(telegram_id, username, chat_id):
    """Add a new user to the database with a starting balance of 0.00 and chat ID."""
    try:
        normalized_username = username.lower()
        cursor.execute("INSERT INTO users (telegram_id, username, balance, chat_id) VALUES (?, ?, ?, ?)", 
                       (telegram_id, normalized_username, 0.00, chat_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:  # Handle if user already exists
        return False

def update_username(telegram_id, new_username, chat_id):
    """Update the username of an existing user in a specific chat."""
    cursor.execute("UPDATE users SET username = ? WHERE telegram_id = ? AND chat_id = ?", 
                   (new_username, telegram_id, chat_id))
    conn.commit()

def add_fund(telegram_id, amount, chat_id):
    """Add funds to a user's balance in a specific chat."""
    cursor.execute("UPDATE users SET balance = balance + ? WHERE telegram_id = ? AND chat_id = ?", 
                   (amount, telegram_id, chat_id))
    conn.commit()

def deduct_fund(telegram_id, amount, chat_id):
    """Deduct funds from a user's balance in a specific chat."""
    cursor.execute("UPDATE users SET balance = balance - ? WHERE telegram_id = ? AND chat_id = ?", 
                   (amount, telegram_id, chat_id))
    conn.commit()

def get_balance(telegram_id, chat_id):
    """Retrieve the balance of a user in a specific chat."""
    cursor.execute("SELECT balance FROM users WHERE telegram_id = ? AND chat_id = ?", (telegram_id, chat_id))
    result = cursor.fetchone()
    return result[0] if result else None

def get_all_balances(chat_id):
    """Retrieve all users' balances from the database for a specific chat."""
    cursor.execute("SELECT username, balance, telegram_id FROM users WHERE chat_id = ?", (chat_id,))
    return cursor.fetchall()

def get_user_id_by_username(username, chat_id):
    """Retrieve the Telegram ID of a user by their username and chat ID."""
    cursor.execute("SELECT telegram_id FROM users WHERE username = ? AND chat_id = ?", (username, chat_id))
    result = cursor.fetchone()
    return result[0] if result else None

def get_users_by_prefix(prefix, chat_id):
    """Retrieve users whose usernames start with the provided prefix in a specific chat."""
    cursor.execute("SELECT username, balance, telegram_id FROM users WHERE username LIKE ? AND chat_id = ?", 
                   (prefix + '%', chat_id))
    return cursor.fetchall()
