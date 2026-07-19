import sqlite3

conn = sqlite3.connect("social.db")
cur = conn.cursor()

with open("USERS.txt") as file:
    cur.execute("DELETE FROM Users")
    for row in file:
        row = row.split(",")
        print(row)
        cur.execute(f"""
INSERT OR IGNORE INTO Users
(UserID,Name,Email,Gender,DateOfBirth,YearOfRegistration,ActiveUser)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

with open("PHASEBOOK.txt") as file:
    cur.execute("DELETE FROM Phasebook")
    for row in file:
        row = row.split(",")
        cur.execute(f"""
INSERT OR IGNORE INTO Phasebook
(UserID,Friends,DateLogin)
VALUES (?, ?, ?)
""", (row[0], row[1], row[2]))

with open("VIEWTUBE.txt") as file:
    cur.execute("DELETE FROM Viewtube")
    for row in file:
        row = row.split(',')
        cur.execute(f"""
INSERT OR IGNORE INTO Viewtube
(UserID,Subscribers,DateLogin)
VALUES (?, ?, ?)
""", (row[0], row[1], row[2]))

with open("WHATSUP.txt") as file:
    cur.execute("DELETE FROM Whatsup")
    for row in file:
        row = row.split(',')
        cur.execute(f"""
INSERT OR IGNORE INTO Whatsup
(UserID,Contacts,DateLogin)
VALUES (?, ?, ?)
""", (row[0], row[1], row[2]))

conn.commit()
print("successfully inserted all records into database")
