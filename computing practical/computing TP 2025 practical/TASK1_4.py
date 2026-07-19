from flask import Flask, render_template, url_for, redirect, request
import sqlite3

app = Flask(__name__)
ac = ['POST', 'GET']

@app.route("/", methods=ac)
def home():
    if request.method:
        print(f"received request")
        if request.method == 'POST':
            return redirect(url_for('home'))
        else:
            return render_template('home.html')

@app.route("/search", methods=ac)
def search():
    if request.method:
        stu_name = request.form["stu_name"].strip().lower()
        conn = sqlite3.connect('college.db')
        cur = conn.cursor()
        cur.execute("""
SELECT Late.date, Late.reason
FROM Late LEFT OUTER JOIN Student ON Late.stu_id = Student.stu_id
WHERE Student.name LIKE ?
ORDER BY Late.date ASC;
""", (stu_name,))
        results = cur.fetchall()
        conn.close()
        return render_template('search.html', results=results, stu_name=stu_name)


app.run(port=6767)
