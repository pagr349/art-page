from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import re

app = Flask(__name__)

# Ensure database folder exists
os.makedirs("database", exist_ok=True)

DB_PATH = "database/messages.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

def is_valid_name(name):
    return re.match("^[A-Za-z\s]{1,50}$", name)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_message(message):
    return len(message) <= 1000

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        honeypot = request.form.get("honeypot")

        if honeypot:
            return "Spam detected.", 400
        
        if not (is_valid_name(name) and is_valid_email(email) and is_valid_message(message)):
            return "Invalid input. Please try again.", 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
                       (name, email, message))
        conn.commit()
        conn.close()

        return redirect(url_for('thanks'))
    return render_template("contact.html")

@app.route('/thanks')
def thanks():
    return render_template("thanks.html")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
