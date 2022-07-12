from flask import Flask, render_template, redirect, jsonify, request, session
from dotenv import load_dotenv

import os

import database

if os.path.isfile(".env"):
    load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
database = database.Database()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new', methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    name = request.form["name"]
    password = request.form["key"]
    page = database.new_page(name, password)
    if page:
        session['user'] = page
        return redirect("/")
    return jsonify({'error': 'name already exists'})

if __name__ == "__main__":
    app.run(debug=True)