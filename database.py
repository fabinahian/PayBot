import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('fund_management.db', check_same_thread=False)
cursor = conn.cursor()

# Create the necessary tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,        
        telegram_id INTEGER UNIQUE,         
        username TEXT UNIQUE,               
        balance REAL DEFAULT 0.00           
    )
''')
conn.commit()

def reset_all_users():
    """Reset the database, removing all users."""
    cursor.execute("DELETE FROM users")
    conn.commit()

def add_user(telegram_id, username):
    """Add a new user to the database with a starting balance of 0.00."""
    try:
        cursor.execute("INSERT INTO users (telegram_id, username) VALUES (?, ?)", (telegram_id, username))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def update_username(telegram_id, new_username):
    """Update the username of an existing user."""
    cursor.execute("UPDATE users SET username = ? WHERE telegram_id = ?", (new_username, telegram_id))
    conn.commit()

def add_fund(telegram_id, amount):
    """Add funds to a user's balance."""
    cursor.execute("UPDATE users SET balance = balance + ? WHERE telegram_id = ?", (amount, telegram_id))
    conn.commit()

def deduct_fund(telegram_id, amount):
    """Deduct funds from a user's balance."""
    cursor.execute("UPDATE users SET balance = balance - ? WHERE telegram_id = ?", (amount, telegram_id))
    conn.commit()

def get_balance(telegram_id):
    """Retrieve the balance of a user."""
    cursor.execute("SELECT balance FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_all_balances():
    """Retrieve all users' balances from the database."""
    cursor.execute("SELECT username, balance, telegram_id FROM users")
    return cursor.fetchall()

def get_user_id_by_username(username):
    """Retrieve the Telegram ID of a user by their username."""
    cursor.execute("SELECT telegram_id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_users_by_prefix(prefix):
    """Retrieve users whose usernames start with the provided prefix."""
    cursor.execute("SELECT username, balance, telegram_id FROM users WHERE username LIKE ?", (prefix + '%',))
    return cursor.fetchall()
