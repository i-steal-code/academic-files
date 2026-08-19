CREATE TABLE "MonitorInfo" (
	"ModelNo"	TEXT,
	"Price"	REAL NOT NULL,
	"Promotion"	INTEGER NOT NULL CHECK("Promotion" > 0 AND "Promotion" <= 100),
	"ScreenSize"	INTEGER NOT NULL,
	"Resolution"	TEXT NOT NULL,
	PRIMARY KEY("ModelNo")
);

CREATE TABLE "ProductInfo" (
	"SerialNo"	TEXT,
	"ModelNo"	TEXT NOT NULL,
	"Status"	TEXT NOT NULL CHECK("Status" = "Sold" OR "Status" = "In Stock"),
	PRIMARY KEY("SerialNo"),
	FOREIGN KEY("ModelNo") REFERENCES "MonitorInfo"("ModelNo")
);

CREATE TABLE "CustomerInfo" (
	"Email"	TEXT,
	"Name"	TEXT NOT NULL,
	"Contact"	TEXT NOT NULL,
	"Address"	TEXT NOT NULL,
	PRIMARY KEY("Email")
);

CREATE TABLE "SalesRecord" (
	"RecordID"	INTEGER,
	"Email"	TEXT NOT NULL,
	"SerialNo"	TEXT NOT NULL,
	"OrderDate"	TEXT NOT NULL,
	"DeliveryDate"	TEXT NOT NULL,
	FOREIGN KEY("Email") REFERENCES "Customer"("Email"),
	FOREIGN KEY("SerialNo") REFERENCES "ProductInfo"("SerialNo"),
	PRIMARY KEY("RecordID" AUTOINCREMENT)
);