from flask import Flask, request, jsonify, render_template
import sqlite3
from model import recommend

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("index.html")

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
