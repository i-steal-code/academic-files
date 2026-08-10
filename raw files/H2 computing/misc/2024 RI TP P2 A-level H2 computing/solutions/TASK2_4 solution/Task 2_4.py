from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transactions', methods=['POST'])
def transactions():
    transaction_type = request.form['transaction_type']
    transaction_date = request.form['transaction_date']
    print(transaction_type, transaction_date)
    conn = sqlite3.connect('../grocery.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT p.ProductName, t.Quantity 
                      FROM transactions t 
                      INNER JOIN products p ON t.ProductID = p.ProductID 
                      WHERE t.TransactionType = ? AND t.TransactionDate = ?
                      ORDER BY t.Quantity DESC''', (transaction_type, transaction_date))
    transactions = cursor.fetchall()
    conn.close()
    
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run()
