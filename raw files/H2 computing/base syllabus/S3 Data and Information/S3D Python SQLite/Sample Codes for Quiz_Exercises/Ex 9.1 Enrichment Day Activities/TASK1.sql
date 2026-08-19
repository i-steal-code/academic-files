BEGIN TRANSACTION;
DROP TABLE IF EXISTS `Sports`;
CREATE TABLE IF NOT EXISTS `Sports` (
	`StudentID`	TEXT,
	`Contact`	TEXT,
	`Cost`	REAL,
	PRIMARY KEY(`StudentID`),
	FOREIGN KEY(`StudentID`) REFERENCES `Registration`(`StudentID`)
);
DROP TABLE IF EXISTS `Registration`;
CREATE TABLE IF NOT EXISTS `Registration` (
	`StudentID`	TEXT,
	`Type`	TEXT,
	`Venue`	TEXT,
	`Session`	TEXT,
	PRIMARY KEY(`StudentID`)
);
DROP TABLE IF EXISTS `Cultural`;
CREATE TABLE IF NOT EXISTS `Cultural` (
	`StudentID`	TEXT,
	`Race`	TEXT,
	PRIMARY KEY(`StudentID`),
	FOREIGN KEY(`StudentID`) REFERENCES `Registration`(`StudentID`)
);
DROP TABLE IF EXISTS `Arts`;
CREATE TABLE IF NOT EXISTS `Arts` (
	`StudentID`	TEXT,
	`Performance`	INTEGER,
	PRIMARY KEY(`StudentID`),
	FOREIGN KEY(`StudentID`) REFERENCES `Registration`(`StudentID`)
);
COMMIT;
