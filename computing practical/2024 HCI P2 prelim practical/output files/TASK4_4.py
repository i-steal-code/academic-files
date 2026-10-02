from flask import Flask, render_template, redirect, request, url_for
import sqlite3

app = Flask(__name__)
ac = ['GET', 'POST']

def get_db():
    conn = sqlite3.connect('TRIP.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods = ac)
def home():
    error = None
    if request.method == 'POST':
        date = request.form.get('date','')
        if date:
            return redirect(url_for('results', date = date))
        error = 'Please fill in all fields'
    return render_template('home.html', error = error)

@app.route('/results/<date>', methods = ac)
def results(date):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    SELECT Customer.Name, Flight.DepartCity, Flight.ArrivalCity, Ticket.Seat
    FROM Customer INNER JOIN Ticket ON Customer.CustomerNo = Ticket.CustomerNo
    INNER JOIN Flight ON Flight.FlightNo = Ticket.FlightNo
    WHERE Ticket.Date = ?
    """, (int(date.strip()),))
    result = cur.fetchall()
    return render_template('results.html', result = result)


if __name__ == '__main__':
    app.run(port=5000)
