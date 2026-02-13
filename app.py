from flask import Flask, render_template, request, redirect
import sqlite3

DATABASE = 'database.db'
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')

def index():
    conn = get_db_connection()
    expenses = conn.execute('select * from expenses').fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]

        conn = get_db_connection()
        conn.execute(
            "insert into expenses (title, amount, category, date) values(?,?,?,?)", (title, amount, category, date)
            )
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('add_expense.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)