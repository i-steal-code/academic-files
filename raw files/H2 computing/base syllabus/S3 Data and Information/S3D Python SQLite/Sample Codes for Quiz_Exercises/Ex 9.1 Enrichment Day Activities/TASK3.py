import sqlite3
conn = sqlite3.connect("register.db")
session = input("Which session (AM/PM)? ")
cursor = conn.execute("SELECT * FROM Registration WHERE Session = ?",(session,))
rows = cursor.fetchall()
print("{:<10}{:<10}{:<10}{:<10}".format("StudentID","Type","Venue","Session"))
for row in rows:
    print("{:<10}{:<10}{:<10}{:<10}".format(row[0],row[1],row[2],row[3]))
conn.close()
