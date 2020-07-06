BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "tags" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT,
	"register_typeid"	INTEGER,
	"address"	INTEGER,
	"scaling"	INTEGER,
	"data_type"	INTEGER,
	"data_size"	INTEGER,
	"tag_groupid"	INTEGER,
	FOREIGN KEY("register_typeid") REFERENCES "variables"("id")
);
CREATE TABLE IF NOT EXISTS "taggroups" (
	"id"	TEXT UNIQUE,
	"plcid"	INTEGER,
	"machineid"	INTEGER,
	"collection_method"	TEXT,
	"collection_type"	TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY("machineid") REFERENCES "machine"("id"),
	FOREIGN KEY("plcid") REFERENCES "controller"("id")
);
CREATE TABLE IF NOT EXISTS "variables" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT,
	"range_start"	INTEGER,
	"range_lower"	INTEGER,
	"plcid"	INTEGER,
	FOREIGN KEY("plcid") REFERENCES "controller"("id")
);
CREATE TABLE IF NOT EXISTS "machine" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT,
	"manualid"	INTEGER,
	"plcid"	INTEGER,
	FOREIGN KEY("plcid") REFERENCES "controller"("id")
);
CREATE TABLE IF NOT EXISTS "connection" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"connection_string"	TEXT,
	"driverid"	INTEGER,
	"plcid"	INTEGER,
	FOREIGN KEY("driverid") REFERENCES "driver"("id"),
	FOREIGN KEY("plcid") REFERENCES "controller"("id")
);
CREATE TABLE IF NOT EXISTS "driver" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT UNIQUE,
	"format"	TEXT
);
CREATE TABLE IF NOT EXISTS "controller" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT UNIQUE,
	"description"	TEXT
);
INSERT INTO "driver" VALUES (1,'Modbus TCP','IPADDRESS;PORT');
INSERT INTO "driver" VALUES (2,'Modbus RTU','DEVICE_PORT;BAUDRATE;PARITY;DATA_BITS;STOP_BITS');
INSERT INTO "controller" VALUES (4,'plc1','details');
INSERT INTO "controller" VALUES (5,'plc2','details');
INSERT INTO "controller" VALUES (6,'plc3','details');
COMMIT;
