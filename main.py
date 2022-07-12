from flask import Flask, render_template, redirect, jsonify, request
from dotenv import load_dotenv

import os

import database

if os.path.isfile(".env"):
    load_dotenv()

app = Flask(__name__)
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
    if database.new_page(name, password):
        return redirect("/")
    return jsonify({'error': 'name already exists'})

if __name__ == "__main__":
    app.run(debug=True)