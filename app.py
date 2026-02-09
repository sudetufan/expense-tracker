from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Expense tracker API is running."

if __name__ == '__main__':
    app.run(debug=True, port=5001)