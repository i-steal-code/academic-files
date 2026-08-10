from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DB = "LIBRARY.db"

@app.route("/", methods=["GET", "POST"])
def search():
    msg = ""
    records = []
    
    if request.method == "POST":
        name = request.form.get("name")

        # query DB
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT Latecoming.date, Latecoming.reason
        FROM Student
        INNER JOIN Latecoming
        ON Student.stu_id = Latecoming.stu_id
        WHERE Student.name = ?
        ORDER BY Latecoming.date DESC;
        """, (name,))
        # fetch
        records = cursor.fetchall()
        conn.close()
            
        return render_template("index.html", records=records, name=name)

    # GET method
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
