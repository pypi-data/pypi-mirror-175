/*
This SQL file builds a test sample that can be used to perform unit tests
against.
*/

BEGIN TRANSACTION;

/* SCHEMA */
CREATE TABLE IF NOT EXISTS "testreal" (
	"realPrimaryKey"	REAL NOT NULL UNIQUE,
	"realNonNull"	REAL NOT NULL,
	"realNull"	REAL,
	"realUnique"	REAL NOT NULL UNIQUE,
	PRIMARY KEY("realPrimaryKey")
);
CREATE TABLE IF NOT EXISTS "testint" (
	"intPrimaryKey"	INTEGER NOT NULL UNIQUE,
	"intNonNull"	INTEGER NOT NULL,
	"intNull"	INTEGER,
	"intUnique"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("intPrimaryKey" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "testblob" (
	"blobPrimaryKey"	BLOB NOT NULL UNIQUE,
	"blobNonNull"	BLOB NOT NULL,
	"blobNull"	BLOB,
	"blobUnique"	BLOB NOT NULL UNIQUE,
	PRIMARY KEY("blobPrimaryKey")
);
CREATE TABLE IF NOT EXISTS "testtext" (
	"textPrimaryKey"	TEXT NOT NULL UNIQUE,
	"textNonNull"	TEXT NOT NULL,
	"textNull"	TEXT,
	"textUnique"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("textPrimaryKey")
);

/* DATA */
INSERT INTO "testreal" 
	("realPrimaryKey","realNonNull","realNull","realUnique") 
VALUES 
	(1.0,1.5,NULL,-5.0);
INSERT INTO "testint" 
	("intPrimaryKey","intNonNull","intNull","intUnique") 
VALUES 
	(1,100,NULL,1000);
INSERT INTO "testblob" 
	("blobPrimaryKey","blobNonNull","blobNull","blobUnique") 
VALUES 
	(x'beef',x'feed',NULL,x'deaf');
INSERT INTO "testtext" 
	("textPrimaryKey","textNonNull","textNull","textUnique") 
VALUES 
	('KEY','HELLO',NULL,'WORLD');
COMMIT;
