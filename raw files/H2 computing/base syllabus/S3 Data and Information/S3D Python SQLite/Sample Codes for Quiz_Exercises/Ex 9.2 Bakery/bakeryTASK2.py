import sqlite3
conn = sqlite3.connect("bakery.db")

#Read from CAKE file and insert data into the bakery database
file = open("CAKES.TXT",'r')
try:
    for line in file:
        ProductCode, Name, Location, Price, ServingSize, Shape = line.strip().split(',')
        conn.execute("INSERT INTO Product VALUES (?,?,?,?,?)",
                     (ProductCode, Name, "CAKE", Location, Price))
        conn.execute("INSERT INTO Cake VALUES (?,?,?)",
                     (ProductCode, ServingSize, Shape))
        conn.commit()
    print("CAKE info successfully updated in database.")
except:
    print("Unable to update CAKE info in database.")
file.close()

#Read from LOAVES file and insert data into the bakery database
file = open("LOAVES.TXT",'r')
try:
    for line in file:
        ProductCode, Name, Location, Price, Weight = line.strip().split(',')
        conn.execute("INSERT INTO Product VALUES (?,?,?,?,?)",
                     (ProductCode, Name, "LOAF", Location, Price))
        conn.execute("INSERT INTO Loaf VALUES (?,?)",
                     (ProductCode, Weight))
        conn.commit()
    print("LOAVES info successfully updated in database.")
except:
    print("Unable to update LOAVES info in database.")
file.close()

#Read from BUNS file and insert data into the bakery database
file = open("BUNS.TXT",'r')
try:
    for line in file:
        ProductCode, Name, Location, Price, PiecesPerPackage = line.strip().split(',')
        conn.execute("INSERT INTO Product VALUES (?,?,?,?,?)",
                     (ProductCode, Name, "BUN", Location, Price))
        conn.execute("INSERT INTO BUN VALUES (?,?)",
                     (ProductCode, PiecesPerPackage))
        conn.commit()
    print("BUNS info successfully updated in database.")
except:
    print("Unable to update BUNS info in database.")
file.close()

conn.close()
