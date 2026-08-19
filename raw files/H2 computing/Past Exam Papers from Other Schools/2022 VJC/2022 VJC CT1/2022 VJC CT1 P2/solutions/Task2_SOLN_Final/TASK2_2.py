import sqlite3
import csv

connection = sqlite3.connect("CarpetsDetails.db")
cursor = connection.cursor()

DiscountsLst = [0.1, 0.1, 0.3]

'''
#with statement will automatically call close() to close the file upon execution
with open("Outlets.txt") as OutletsFile: 
        #data = OutletsFile.readlines()
        #for row in data:
        for row in OutletsFile:
                lst = row.strip().split(",")
                cursor.execute("INSERT OR IGNORE INTO Outlets VALUES (?, ?)",(int(lst[0]), lst[1]))

with open("Carpets.txt") as CarpetsFile:
        #data = CarpetsFile.readlines()
        #for row in data:
        for row in CarpetsFile:
                lst = row.strip().split(",")
                cursor.execute("INSERT OR IGNORE INTO Carpets VALUES (?, ?, ?, ?, ?, ?)",\
                               (int(lst[0]), float(lst[1]), lst[2], lst[3], lst[4], lst[5]))
                cursor.execute("INSERT OR IGNORE INTO Promotion VALUES (?, ?, ?)",\
                               (int(lst[5]), int(lst[0]), float(lst[1])))
'''

#with statement will automatically call close() to close the file upon execution
with open("Outlets.txt") as OutletsFile:
        reader = csv.reader(OutletsFile)
        for lst in reader:
                cursor.execute("INSERT OR IGNORE INTO Outlets VALUES (?, ?)",(int(lst[0]), lst[1]))

with open("Carpets.txt") as CarpetsFile:
        reader = csv.reader(CarpetsFile)
        for lst in reader:
                cursor.execute("INSERT OR IGNORE INTO Carpets VALUES (?, ?, ?, ?, ?)",\
                               (int(lst[0]), round(float(lst[1]),2), lst[2], lst[3], int(lst[4])))
                cursor.execute("INSERT OR IGNORE INTO Promotion VALUES (?, ?, ?)",\
                               (int(lst[0]), int(lst[4]), round(float(lst[1]),2)))

for Outlet in range(len(DiscountsLst)):
	cursor.execute('''
		UPDATE Promotion
		SET DiscountedPrice = DiscountedPrice * ?
		WHERE OutletID = ?
		''', (1-DiscountsLst[Outlet], Outlet+1))

connection.commit()
connection.close()		


#open file and connect database
#close file, save and close database
#read Outlets.txt and insert into Outlets Table
#read Carpets.txt and insert into Carpets Table
#insert correct data in Promotions Table
##correct discounted price inserted
