BEGIN TRANSACTION;
DROP TABLE IF EXISTS "user_details";
CREATE TABLE IF NOT EXISTS "user_details" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"roleid"	INTEGER NOT NULL,
	FOREIGN KEY("roleid") REFERENCES "user_roles"("id")
);
DROP TABLE IF EXISTS "user_roles";
CREATE TABLE IF NOT EXISTS "user_roles" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE
);
DROP TABLE IF EXISTS "SystemSettings";
CREATE TABLE IF NOT EXISTS "SystemSettings" (
	"MongoDBAddress"	TEXT NOT NULL
);
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
INSERT INTO "user_details" ("id","name","password","roleid") VALUES (1,'admin','admin',1);
INSERT INTO "user_roles" ("id","name") VALUES (1,'admin'),
 (2,'user');
INSERT INTO "SystemSettings" ("MongoDBAddress") VALUES ('mongodb://localhost:27017');
INSERT INTO "register_types" ("id","ragister_type","range_upper","range_lower") VALUES (1,'Output coils',1,9999),
 (2,'Discrete inputs',10001,19999),
 (3,'Input Registers',30001,39999),
 (4,'Holding registers',40001,49999);
INSERT INTO "driver" ("id","name","format") VALUES (1,'Modbus RTU','COMPORT;BAUDRATE;PARITY;BYTESIZE;STOPBITS'),
 (2,'Modbus TCP','IPADDRESS;PORT');
COMMIT;
