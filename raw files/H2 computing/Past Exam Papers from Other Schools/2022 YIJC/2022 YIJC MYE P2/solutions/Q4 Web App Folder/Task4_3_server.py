from flask import Flask, render_template, request

from sqlite3 import *

app = Flask(__name__)

@app.route('/')
def index():
    db = connect("StoreSG.db")
    c = db.cursor()
    c.execute('''SELECT * FROM Product;''')  #1m connect and execute
    products = c.fetchall()
    db.close()              #1m correct code to render html
                            #1m correct variables sent
    return render_template("Task4_3_index.html",products=products) 
                            #2m in html file (1m jinja code correct)
                            #                (1m html correct)
app.run("127.0.0.1", port=5000)
