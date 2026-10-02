from flask import Flask, render_template, url_for, redirect, request
import sqlite3

app = Flask(__name__)
ac = ['GET', 'POST']

def get_db():
    conn = sqlite3.connect('BUSROUTES.db')
    conn.row_factory = sqlite3.Row
    return conn

#web app routing
@app.route('/', methods = ac)
def home():
    error = None
    if request.method == 'POST':
        bus_code = request.form.get('bus_code','')
        if bus_code:
            return redirect(url_for('results', bus_code = bus_code))
        error = 'Please fill in all fields'
    return render_template('home.html', error = error)

@app.route('/results/<bus_code>', methods = ac)
def results(bus_code):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT ServiceNo, Operator
        FROM Route
        WHERE BusStopCode = ?
    """, (bus_code,))
    output = cur.fetchall()
    return render_template('results.html', output = output)

if __name__ == '__main__':
    app.run(port=5000)
    
