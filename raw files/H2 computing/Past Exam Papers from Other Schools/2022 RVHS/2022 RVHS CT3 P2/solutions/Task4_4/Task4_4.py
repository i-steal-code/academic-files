from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

curr_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(curr_dir, "spectrum.db")


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/warranty/", methods=["GET", "POST"])
def warranty():
    if request.method == "GET":
        return render_template('warranty.html')
    else:
        serial_no = request.form["serial_no"]

        db = sqlite3.connect(db_file)
        query = """
SELECT ProductInfo.SerialNo, MonitorInfo.ModelNo, 
ScreenSize, Resolution, OrderDate, Email
FROM MonitorInfo, ProductInfo, SalesRecord
WHERE MonitorInfo.ModelNo = ProductInfo.ModelNo
AND ProductInfo.SerialNo = SalesRecord.SerialNo
AND ProductInfo.SerialNo = ?
        """
        cursor = db.execute(query, (serial_no,))
        record = cursor.fetchone()

        cursor.close()
        db.close()

        return render_template(
            "ack.html",
            record=record)


if __name__ == '__main__':
    app.run(debug=False)
