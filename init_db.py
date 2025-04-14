import sqlite3

conn = sqlite3.connect('cashtrack.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
''')

# Create transactions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Optional: Pre-fill with common categories
categories = [
    ('income', 'Salary'),
    ('income', 'Gift'),
    ('expense', 'Food'),
    ('expense', 'Rent'),
    ('expense', 'Shopping'),
    ('expense', 'Travel')
]

# Optional table (not essential if categories are stored directly in transactions)
cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
    name TEXT NOT NULL
)
''')

cursor.executemany('INSERT INTO categories (type, name) VALUES (?, ?)', categories)

conn.commit()
conn.close()

print("Database initialized and ready.")
