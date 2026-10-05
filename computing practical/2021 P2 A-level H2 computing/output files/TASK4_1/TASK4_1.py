from flask import Flask, redirect, url_for, render_template, request
import sqlite3

app = Flask(__name__)
ac = ['GET', 'POST']

def get_db():
    conn = sqlite3.connect('Task4.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods = ac)
def home():
    return render_template('home.html')

@app.route('/display/<rounds>', methods = ac)
def display(rounds):
    results = []
    rounds = str(rounds)
    if rounds.isnumeric():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        SELECT competitor.name, scores.score
        FROM competitor INNER JOIN scores ON competitor.id = scores.id
        WHERE scores.round = ?
        ORDER BY scores.score DESC
        """, (rounds,))
        for row in cur.fetchall():
            results.append([row['name'],row['score']])
    elif rounds == 'mean':
        conn = sqlite3.connect('Task4.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT competitor.name, SUM(scores.score)/MAX(scores.round)
        FROM competitor INNER JOIN scores ON competitor.id = scores.id
        GROUP BY competitor.name 
        ORDER BY competitor.name ASC
        """)
        results = cur.fetchall()
    elif rounds == 'qualifiers':
        conn = sqlite3.connect('Task4.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT competitor.name, SUM(scores.score), SUM(scores.score) > 250
        FROM competitor INNER JOIN scores ON competitor.id = scores.id
        GROUP BY competitor.name 
        ORDER BY SUM(scores.score) DESC
        """)
        for row in cur.fetchall():
            row = list(row)
            if int(row[2]) == 1:
                row[2] = 'qualified'
            else:
                row[2] = 'did not qualify'
            results.append(row)
        
    return render_template('display.html', results = results, rounds = rounds)

if __name__ == '__main__':
    app.run(port=5000)
