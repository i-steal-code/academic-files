import sqlite3
conn = sqlite3.connect("register.db")

while True:
    StudentID = input("Enter StudentID: ")
    Venue     = input("Enter venue: ")
    Session   = input("Enter session (AM/PM): ")
    Type      = input("Enter type (A/C/S): ")

    conn.execute("""INSERT INTO Registration VALUES (?,?,?,?)""",
                 (StudentID, Type, Venue, Session))
    conn.commit() #write changes to database

    if Type == 'A':
        performance = int(input("Enter 1 for Performance arts, 0 for Visual arts: "))
        conn.execute("INSERT INTO Arts VALUES (?,?)",(StudentID,performance))
    elif Type == 'C':
        race = input ("Enter race (Chinese/Malay/Indian/Others): ")
        conn.execute("INSERT INTO Cultural VALUES (?,?)",(StudentID, race))
    elif Type == 'S':
        contact = input("Enter C for contact, NC for non-contact sports: ")
        cost    = float(input("Enter cost of activity: "))
        conn.execute("INSERT INTO Sports VALUES (?,?,?)",(StudentID, contact, cost))
    conn.commit()
    anymore = input("Any more data to enter (Y/N)?")
    if anymore[0].upper() != 'Y':
        break
conn.close()


