BEGIN TRANSACTION;
DROP TABLE IF EXISTS "tag_group_mapping";
CREATE TABLE IF NOT EXISTS "tag_group_mapping" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"tag_group_id"	INTEGER NOT NULL,
	"tag_id"	INTEGER NOT NULL,
	FOREIGN KEY("tag_id") REFERENCES "tags"("id"),
	FOREIGN KEY("tag_group_id") REFERENCES "taggroups"("id")
);
DROP TABLE IF EXISTS "taggroups";
CREATE TABLE IF NOT EXISTS "taggroups" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"plcid"	INTEGER,
	"machineid"	INTEGER,
	"collection_method"	INTEGER,
	"collection_type"	TEXT,
	FOREIGN KEY("machineid") REFERENCES "machine"("id"),
	FOREIGN KEY("plcid") REFERENCES "controller"("id")
);
DROP TABLE IF EXISTS "tags";
CREATE TABLE IF NOT EXISTS "tags" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"register_typeid"	INTEGER,
	"address"	INTEGER,
	"scaling"	INTEGER,
	"data_type"	INTEGER,
	"data_size"	INTEGER,
	FOREIGN KEY("register_typeid") REFERENCES "register_types"("id")
);
DROP TABLE IF EXISTS "register_types";
CREATE TABLE IF NOT EXISTS "register_types" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"ragister_type"	TEXT,
	"range_upper"	INTEGER,
	"range_lower"	INTEGER
);
DROP TABLE IF EXISTS "machine";
CREATE TABLE IF NOT EXISTS "machine" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT,
	"manualid"	INTEGER,
	"plcid"	INTEGER,
	FOREIGN KEY("plcid") REFERENCES "controller"("id")
);
DROP TABLE IF EXISTS "driver";
CREATE TABLE IF NOT EXISTS "driver" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"format"	TEXT
);
DROP TABLE IF EXISTS "connection";
CREATE TABLE IF NOT EXISTS "connection" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"connection_string"	TEXT NOT NULL,
	"driverid"	INTEGER,
	"plcid"	INTEGER,
	FOREIGN KEY("driverid") REFERENCES "driver"("id"),
	FOREIGN KEY("plcid") REFERENCES "controller"("id")
);
DROP TABLE IF EXISTS "controller";
CREATE TABLE IF NOT EXISTS "controller" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"description"	TEXT
);
COMMIT;
