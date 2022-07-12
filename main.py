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
    if 'user' not in session:
        return render_template("index.html")
    return render_template("user.html", user=session['user'])

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

@app.route('/verify')
def verify():
    name = request.args["name"]
    password = request.args["key"]
    page = database.get_page(name, password)
    if page:
        session['user'] = page
        return redirect("/")
    return jsonify({'error': 'invalid name or password'})

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)