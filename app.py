from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random


app = Flask(__name__)


users = {
    "admin"  : "password"
}

conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS reports(
               id integer,
               title text,
               description text,
               amount REAL
            );""")



@app.route('/')
def index():
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in users and users[username] == password:
        # Successful login, redirect to some other page
        return redirect(url_for('home'))
    else:
        # Failed login, redirect back to login page with an error message
        return render_template('login.html', error="Invalid username or password")

@app.route("/home")
def home():
    amount_total = 0
    cursor.execute("SELECT * FROM reports")
    rows = cursor.fetchall()

    print(rows)

    for i in rows:
        amount_total += float(i[3])


    return render_template('home.html', account_total=str(amount_total), entries=rows)

@app.route("/create-record")
def create_record_page():
    return render_template("create-record.html")

@app.route("/add-record", methods=['POST'])
def add_record():
    cursor = conn.cursor()
    title = request.form.get("title")
    description = request.form.get("description")
    amount = request.form.get("amount")

    cursor.execute("INSERT INTO reports(id, title, description, amount) VALUES (?,?,?,?)", (random.randrange(1000, 9999), title, description, float(amount)))
    conn.commit()
    return redirect(url_for("home"))




if __name__ == '__main__':
    app.run(debug=True)