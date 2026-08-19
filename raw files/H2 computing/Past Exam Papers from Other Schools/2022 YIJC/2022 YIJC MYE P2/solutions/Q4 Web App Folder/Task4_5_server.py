from flask import Flask, render_template, request

from sqlite3 import *

app = Flask(__name__)

### Task 4.3 #########################################################

@app.route('/')
def index():
    db = connect("StoreSG.db")
    c = db.cursor()
    c.execute('''SELECT * FROM Product;''')  #1m connect and execute
    products = c.fetchall()
    db.close()              #1m correct code to render html
                            #1m correct variables sent
    return render_template("Task4_4_index.html",products=products) 
                            #2m in 4_3.html file (1m jinja code correct)
                            #                (1m html correct)

### Task 4.5 #########################################################
                                    
@app.route('/ordering', methods = ['POST'])     # 1m correct method
def ordering():
    schoolcode = request.form.get('SchoolCode') # 1m correct retrieve
    productid = request.form.get('ProductID')   #   variables
    qty = request.form.get('Quantity')
    
    db = connect("StoreSG.db")
    c = db.cursor()                 # 1m correct insert with 'Pending'
    c.execute('''INSERT INTO Buy
        (SchoolCode,ProductID,Qty,Status)
        VALUES (?,?,?,'Pending')''',(schoolcode,productid,qty))
                            # students may overcomplicate the BuyID


    
    c.execute('''SELECT * FROM Product WHERE ProductID = ?''', (productid,))
    product = c.fetchone()  # 1m retrieve name and unit cost
    unitcost = product[2]   #    from db, based on productid
    db.commit()
    db.close()
    p = product[1] 
    q = qty
    t = "${:.2f}".format(int(qty)*float(unitcost)) #no penalty for format
                            # including total cost calculation
    
    return render_template("success.html", p=p,q=q,t=t) #1m commit
                                        #   and render successfully
                                                        
app.run("127.0.0.1", 5000, debug=True)
