from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    service TEXT,
                    date TEXT,
                    time TEXT)''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/book", methods=["POST"])
def book():
    name = request.form["name"]
    service = request.form["service"]
    date = request.form["date"]
    time = request.form["time"]

    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("INSERT INTO bookings (name, service, date, time) VALUES (?,?,?,?)",
              (name, service, date, time))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/admin")
def admin():
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    data = c.fetchall()
    conn.close()
    return render_template("admin.html", bookings=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
