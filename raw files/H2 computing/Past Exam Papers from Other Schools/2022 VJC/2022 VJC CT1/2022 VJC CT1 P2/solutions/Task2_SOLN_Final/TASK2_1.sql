CREATE TABLE Outlets(
	OutletID INTEGER PRIMARY KEY,
	Location TEXT
	);
	/*1 mark*/

CREATE TABLE Carpets(
	CarpetID INTEGER PRIMARY KEY,
	OriginalPrice FLOAT,
	Country TEXT,
	Style TEXT,
	OutletID INTEGER REFERENCES Outlets(OutletID)
	);
	/*2 marks*/

CREATE TABLE Promotion(
	CarpetID INTEGER REFERENCES Carpets(CarpetID),
	OutletID INTEGER REFERENCES Outlets(OutletID),
	DiscountedPrice FLOAT,
	PRIMARY KEY(CarpetID, OutletID)
	);
	/*3 marks*/