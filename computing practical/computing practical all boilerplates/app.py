#init, connect and reset
from flask import Flask, render_template, request, redirect, url_for
import sqlite3, pymongo, json, csv

app = Flask(__name__)
accepted_methods = ['GET', 'POST']

conn = sqlite3.connect("database.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS student
""")
cur.execute("""
DROP TABLE IF EXISTS late
""")

print("successfully connected to, initialised and reset database")

#import files into database
with open("STUDENT.csv") as file:
    reader = csv.reader(file)
    headers = next(reader)
    cur.execute(f"""
CREATE TABLE IF NOT EXISTS student (
{headers[0]} INTEGER PRIMARY KEY,
{headers[1]} TEXT,
{headers[2]} TEXT,
{headers[3]} INTEGER
)""")
    for row in reader:
        cur.execute(f"""
INSERT OR IGNORE INTO student
{tuple(headers)}
VALUES(?,?,?,?)
""", row)

with open("LATE.csv") as file:
    reader = csv.reader(file)
    headers = next(reader)
    cur.execute(f"""
CREATE TABLE IF NOT EXISTS late (
{headers[0]} TEXT,
{headers[1]} INTEGER,
{headers[2]} TEXT,
FOREIGN KEY({headers[1]}) REFERENCES student({headers[1]})
)""")
    for row in reader:
        cur.execute(f"""
INSERT OR IGNORE INTO late
{tuple(headers)}
VALUES (?,?,?)
""", row)

conn.commit()
print("successfully imported all data into database")

#homepage 
@app.route('/', methods = accepted_methods)
def home():
    error = None
    if request.method:
        print(f"{request.method} request received to home")
    #1. POST
    if request.method == 'POST': 
        category = request.form.get('category', '').strip()
        name = request.form.get('name', '').strip()

        if name and category:
            #2. redirect
            return redirect(url_for('results', category=category, name=name))
        else:
            #error handling: incomplete form
            error = "Please fill in all fields"
    #default GET upon entry
    return render_template('home.html', error=error)

#result page
@app.route('/results/<category>/<name>')
def results(category, name):
    #3. GET
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    #SQL query to display
    cur.execute("""
SELECT student.Student_Name, student.Class_Group, late.Date, late.Reason
FROM student INNER JOIN late ON student.Student_ID = late.Student_ID
WHERE student.Student_Name LIKE ? AND late.Reason = ?
""", (f"%{name}%", category))
    data = cur.fetchall()
    conn.close()
    return render_template("results.html" ,results=data, category=category, name=name)

#run app 
app.run(port=6767)
