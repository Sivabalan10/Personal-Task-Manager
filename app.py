from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create and connect to the database
def get_db_connection():
    conn = sqlite3.connect('records.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the database and user_details table
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = get_db_connection()
    today = datetime.now().strftime('%Y-%m-%d')
    tasks = conn.execute('SELECT * FROM user_details WHERE DATE(timestamp) = ?', (today,)).fetchall()
    conn.close()
    total_tasks = len(tasks)
    return render_template('index.html', tasks=tasks, total_tasks=total_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    if task:
        conn = get_db_connection()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('INSERT INTO user_details (task, timestamp) VALUES (?, ?)', (task, now))
        conn.commit()
        conn.close()
    return redirect(url_for('home'))

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM user_details WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
