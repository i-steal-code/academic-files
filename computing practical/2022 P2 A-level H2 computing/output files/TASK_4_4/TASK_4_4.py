from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)
ac = ['GET', 'POST']

def get_db():
    conn = sqlite3.connect('LIBRARY.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods = ac)
def display():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    SELECT Member.FamilyName, Member.GivenName, Book.Title
    FROM Book INNER JOIN Loan ON Book.BookID = Loan.BookID
    INNER JOIN Member ON Member.MemberNumber = Loan.MemberNumber
    WHERE Loan.Returned = ?
    """, ('FALSE',))
    results = cur.fetchall()
    conn.close()
    return render_template('display.html', results = results)


if __name__ == '__main__':
    app.run(port=5000)
