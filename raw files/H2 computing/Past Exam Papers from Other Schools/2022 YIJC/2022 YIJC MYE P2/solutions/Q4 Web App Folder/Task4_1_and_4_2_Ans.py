# Task 4.1 (5m)

from sqlite3 import *

db = connect("StoreSG.db")              # Connection to database
c = db.cursor()

c.execute('''CREATE TABLE Buy (
                BuyID	        INTEGER NOT NULL PRIMARY KEY Autoincrement,
                SchoolCode	TEXT REFERENCES School(SchoolCode),
                ProductID	INTEGER REFERENCES Product(ProductID),
                Qty	        INTEGER,
                Status          TEXT);''')
                                        #1m SQL Create/Correct data types
                                        #1m with 1 Primary Key
                                        #1m with 2 Foreign Keys
    
f = open("Buy.TXT")                  
next(f)                                 #skip header (correct data extraction)
lines = f.readlines()
for line in lines:                
    line = line.strip().split(',')      #1m correct data extraction
    #print(line)
    c.execute('''INSERT INTO Buy (SchoolCode,ProductID,Qty,Status) VALUES (?, ?, ?, ?)''', line)
                                        #1m correct SQL Insert statement
#db.commit()                            #committed
#db.close()


##################################################################

#Task 4.2a and 4.2b Mark Scheme (5m)
c.execute('''SELECT ProductName, Buy.Qty, Product.UnitCost FROM Product, Buy
WHERE Buy.SchoolCode = 7612
AND Product.ProductID = Buy.ProductID ''')
task42a = c.fetchall()
print(task42a)
#Task 4.2b
c.execute('''SELECT SUM(Buy.Qty* Product.UnitCost) FROM Product, Buy
WHERE Buy.SchoolCode = 7612
AND Product.ProductID = Buy.ProductID''')
task42b = c.fetchone()
print(task42b)

#For both 4.2a and 4.2b (Max 4m out of 5 points)
#1m Use of SELECT …
#1m identify 4 attributes (ProductName, Buy.Qty, Product.UnitCost, Buy.SchoolCode)
#1m Use of FROM with two tables (Item and Buy)
#1m SchoolCode checked in the WHERE clause
#1m Use a JOIN (Product and Buy) table linking by ProductID

#For 4.2b only: (Max 1m out of 1 point)
#1m Use aggregate query SUM(Buy.Qty * Item.UnitCost) for 4.2b

db.commit()
db.close()
