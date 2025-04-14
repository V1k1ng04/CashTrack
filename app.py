from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

DATABASE = 'cashtrack.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Registration successful. Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Handle form submission for income/expense
    if request.method == 'POST':
        transaction_type = request.form['type']
        category = request.form['category']
        amount = float(request.form['amount'])
        date = request.form['date']
        note = request.form['note']
        user_id = session['user_id']

        # Insert the transaction into the database
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO transactions (user_id, type, category, amount, date, note)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, transaction_type, category, amount, date, note))
        conn.commit()
        conn.close()

        flash(f'{transaction_type.capitalize()} of {amount} added successfully!')

    # Get all transactions for the logged-in user
    conn = get_db_connection()
    transactions = conn.execute('''
        SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC
    ''', (session['user_id'],)).fetchall()

    # Calculate all-time totals
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = total_income - total_expenses

    conn.close()

    return render_template('dashboard.html',
                           transactions=transactions,
                           total_income=total_income,
                           total_expenses=total_expenses,
                           balance=balance)

if __name__ == '__main__':
    app.run(debug=True,port=5001)
