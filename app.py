from flask import Flask, request, jsonify, render_template, redirect, session
import sqlite3
import os
from model import recommend

app = Flask(__name__)
app.secret_key = "secret123"

# -------------------------
# DATABASE INIT
# -------------------------
def init_db():
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')

    # default admin
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users VALUES (NULL, 'admin', 'admin123', 'admin')")

    conn.commit()
    conn.close()

# -------------------------
# ROUTES
# -------------------------
@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login-page')
    if session.get('role') != 'user':
        return "Access Denied"
    return render_template('index.html')

@app.route('/login-page')
def login_page():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (data['username'], data['password'], 'user'))
        conn.commit()
        return redirect('/login-page')
    except:
        return "User already exists"

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                (data['username'], data['password']))
    user = cur.fetchone()

    if user:
        session['user'] = user[1]
        session['role'] = user[3]
        if user[3] == 'admin':
            return redirect('/admin')
        return redirect('/')
    return "Invalid credentials"

@app.route('/admin')
def admin():
    if 'user' not in session or session.get('role') != 'admin':
        return "Access Denied"

    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("SELECT username, role FROM users")
    users = cur.fetchall()

    return render_template('admin.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login-page')

@app.route('/add-movie', methods=['POST'])
def add_movie():
    data = request.json
    movie = data['movie']
    recs = recommend(movie)
    return jsonify({"recommendations": recs})

# -------------------------
# RUN
# -------------------------
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
