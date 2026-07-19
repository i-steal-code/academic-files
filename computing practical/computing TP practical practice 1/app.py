from flask import Flask, render_template, request, redirect, url_for
import sqlite3, pymongo

app = Flask(__name__)
accepted = ['GET', 'POST']

@app.route('/', methods=accepted)
def home():
    if request.method == 'POST':
        print("received post request to homepage")
    elif request.method == 'GET':
        print("received GET request to homepage")
    return render_template("home.html")

@app.route('/search', methods=accepted)
def search():
    if request.method == 'POST':
        print("received POST request to results")
        category = request.form['category']
        name = request.form['name']
        print(f"user input is {category, name}")
        if name == '':
            name = "Null"
            return render_template('results.html', category=category, name=name)
        conn = sqlite3.connect('mock_database.db')
        cur = conn.cursor()
        print("successful sqlite3 connection")
        #cur.execute("insert SQL query to SELECT fields with matching category and name. currently left blank as a placeholder")
        #data = cur.fetchall()
        data = "placeholder"
        conn.close()
        if data == "placeholder":
            print("data received from database")
        elif data == '':
            return render_template('results.html', category=category, name=name)
    elif request.method == 'GET':
        print("received GET request to results")
    return render_template('results.html')

app.run(port=5001)
