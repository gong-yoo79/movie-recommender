from flask import Flask, request, jsonify, render_template
import sqlite3
from model import recommend

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()

    # ✅ Existing table (DO NOT REMOVE)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie TEXT
        )
    ''')

    # ✅ New table (ADD THIS)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')

    # ✅ Default admin (ADD THIS)
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ("admin", "admin123", "admin"))

    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("index.html")


# ✅ ADD SIGNUP HERE 👇
@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    username = data['username']
    password = data['password']

    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, password, "user"))
        conn.commit()
        return redirect('/login-page')
    except:
        return "User already exists"

@app.route('/add-movie', methods=['POST'])
def add_movie():
    data = request.json
    movie = data['movie']

    recs = recommend(movie)

    return jsonify({
        "recommendations": recs
    })
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
