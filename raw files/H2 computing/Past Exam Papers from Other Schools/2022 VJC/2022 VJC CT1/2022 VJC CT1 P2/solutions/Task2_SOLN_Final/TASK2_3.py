from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

connection = sqlite3.connect("CarpetsDetails.db")
cursor = connection.cursor()

cursor.execute("SELECT DISTINCT Country FROM Carpets")
COUNTRY = [element[0] for element in cursor.fetchall()]

cursor.execute("SELECT DISTINCT Style FROM Carpets")
STYLE = [element[0] for element in cursor.fetchall()]

connection.commit()
connection.close()

'''
COUNTRY = ["Pakistan", "Turkey", "Afghanistan"]
STYLE = ["Modern", "Contemporary", "Traditional"]
'''

@app.route("/", methods=["GET", "POST"])
def filter():
        if request.method == "POST":
                country = request.form["COUNTRY"]
                style = request.form["STYLE"]
                minPrice = request.form["MINPRICE"]
                maxPrice = request.form["MAXPRICE"]
                
                connection = sqlite3.connect("CarpetsDetails.db")
                cursor = connection.cursor()

                if float(maxPrice) <  float(minPrice):
                        error = "Error. The maximum price must be greater than or equal to the minimum price.\n"
                        return render_template("form.html", COUNTRY=COUNTRY, STYLE=STYLE, error=error)
                
                cursor.execute('''
                                SELECT Carpets.CarpetID, Carpets.Country, Carpets.Style, \
                                printf("%.2f", Promotion.DiscountedPrice) 
                                FROM Carpets
                                INNER JOIN Promotion
                                ON Carpets.CarpetID = Promotion.CarpetID
                                WHERE Carpets.Country = ?
                                AND Carpets.Style = ?
                                AND Promotion.DiscountedPrice >= ?
                                AND Promotion.DiscountedPrice <= ?
                                ''', (country,style,minPrice,maxPrice))
                results = cursor.fetchall()
                
                cursor.close()
                connection.close()
                return render_template("results.html", results=results)
        else:
                return render_template("form.html", COUNTRY=COUNTRY, STYLE=STYLE)
									
if __name__ == "__main__":
	app.run()

#html input to select country
#html input to select design style
	#jinja for loop
#html inputs to enter a price range
#submit button
#discounted price displayed in 2dp
#input validation: max price >= min price
        #appropriate error message
#user to be able to re-input price range
#correct output displayed
        #open database
	#close database
	#function to request html inputs (country, design, price range)
	#INNER JOIN promotion table on carpetID
	#WHERE country, style and price match user inputs
	
