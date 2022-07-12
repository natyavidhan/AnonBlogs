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
    blogs = database.get_blogs(session['user']['_id'])
    blogs.reverse()
    return render_template("user.html", user=session['user'], blogs=blogs)

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

@app.route('/blog/new', methods=["GET", "POST"])
def blog_new():
    if 'user' not in session:
        return redirect("/")
    if request.method == "GET":
        return render_template("blog_new.html")
    title = request.form["title"]
    content = request.form["content"]
    blog = database.new_blog(session['user']['_id'], {'title': title, 'content': content})
    return redirect("/")

@app.route('/p/<page_name>')
def user(page_name):
    user = database.get_page(page_name)
    if user:
        blogs = database.get_blogs(page_name)
        return render_template("profile.html", user=user, blogs=blogs)

if __name__ == "__main__":
    app.run(debug=True)