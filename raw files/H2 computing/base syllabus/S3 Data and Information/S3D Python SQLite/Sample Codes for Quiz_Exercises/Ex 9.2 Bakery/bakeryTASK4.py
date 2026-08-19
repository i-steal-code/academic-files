import sqlite3
conn=sqlite3.connect("bakery.db")
location = input("Enter the location (North/South/East/West): ")
cursor = conn.execute("SELECT Name, Type, Price FROM Product WHERE Location =? ORDER BY Price ASC, Name DESC",
                      (location,))
rows = cursor.fetchall()
for row in rows:
    print(row[0],row[1],row[2])
conn.close()
