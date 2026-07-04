from flask import Flask, render_template, request, redirect, url_for
from itertools import zip_longest
import sqlite3, pymongo

app = Flask(__name__)
ac_meth = ['GET', 'POST']
database = [["placeholder",21,69,67,41,89],[]]


@app.route("/", methods=ac_meth)
def index():
    if request.method == 'POST':
        print("received post request...")
        user_input = request.form['test']
        print(f"user posted {user_input} to index route")
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        print("sqlite3 connection successful")
        #data = cur.fetchall()
        database[0].append(user_input)
        conn.close()
    elif request.method == "GET":
        print("we got a request!")
    rows=list(zip_longest(database[0], database[1], fillvalue=''))
    return render_template("index.html", rows=rows)
@app.route("/new_record", methods=ac_meth)
def new_record():
    if request.method == 'POST' and "thing" in request.form:
        user_input = request.form['thing']
        if user_input == '':
            user_input = "NULL"
        print(f"user posted {user_input} to new_record route")
        return render_template("new_record.html", results=user_input)
    else:
        print("that was not a post request... but we got a 'GET' request")
        return render_template("index.html")
@app.route("/submit_record", methods=ac_meth)
def submit_record():
    try:
        if request.method =='POST' and 'text' in request.form:
            user_input = request.form['text']
            print(f"we got something! user keyed in {user_input}")
            database[1].append(user_input)
        else:
            print("something went wrong but at least we went through to the server!")
        return redirect(url_for("index"))
    except:
        print(f"something went wrong")
@app.route("/late/<data>/")
def late_info(data):
    print(f"late info {data}")
    data=str(data)
    result = "invalid search parameter"
    try:
        if data.isdigit() and len(data)==5:
            result = f"student ID {data} is late"
        elif data[2].lower() == "s" and data[5].isalpha() and len(data) == 6:
            result = f"All students from class {data} are late"
    except:
        pass
    return render_template("late.html", results=result)

app.run(port=5000)
