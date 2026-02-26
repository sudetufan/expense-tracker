from flask import Flask, render_template, request, redirect, url_for
import sqlite3

CATEGORIES = [
    "Yemek",
    "Ulaşım",
    "Eğlence",
    "Alışveriş",
    "Fatura",
    "Diğer"
]

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

    total = conn.execute("select sum(amount) from expenses").fetchone()[0]
    if total is None:
        total = 0

    category_totals = conn.execute("select category, sum(amount) as total from expenses group by category").fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses, total=total, category_totals=category_totals, categories=CATEGORIES)

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
    return render_template('add_expense.html', categories=CATEGORIES)


@app.route("/delete/<int:id>")
def delete_expense(id):
    conn = get_db_connection()
    conn.execute("delete from expenses where id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
