CREATE TABLE Product (ProductCode VARCHAR(10), Name VARCHAR(20), 
Type VARCHAR(10), Location VARCHAR(10), Price REAL, 
PRIMARY KEY (ProductCode) );

CREATE TABLE Cake (ProductCode TEXT, ServingSize INTEGER, Shaper TEXT,
PRIMARY KEY (ProductCode), 
FOREIGN KEY (ProductCode) REFERENCES Product (ProductCode));

CREATE TABLE Loaf (ProductCode TEXT, Weight REAL, 
PRIMARY KEY (ProductCode), 
FOREIGN KEY (ProductCode) REFERENCES Product (ProductCode));

CREATE TABLE Bun (ProductCode TEXT, PiecesPerPackage INTEGER,
PRIMARY KEY (ProductCode),
FOREIGN KEY (ProductCode) REFERENCES Product (ProductCode));