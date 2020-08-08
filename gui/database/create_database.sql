CREATE TABLE "SystemSettings" (
	"MongoDBAddress"	TEXT NOT NULL
)
CREATE TABLE connection
  (id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
   connection_string        TEXT NOT NULL,
   driverid INTEGER,
   plcid       INTEGER,
 

   FOREIGN KEY(plcid)   REFERENCES controller(id),

   FOREIGN KEY(driverid)   REFERENCES driver(id)
   )

CREATE TABLE "controller" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"description"	TEXT
)

CREATE TABLE driver
  (id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
   name        TEXT NOT NULL UNIQUE,
   format      TEXT
)

CREATE TABLE machine
  (id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
   name        TEXT,
   manualid    INTEGER,
   plcid       INTEGER,
 

   FOREIGN KEY(plcid)   REFERENCES controller(id)
   )

CREATE TABLE "register_types" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"ragister_type"	TEXT,
	"range_upper"	INTEGER,
	"range_lower"	INTEGER
)

CREATE TABLE "tag_group_mapping" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"tag_group_id"	INTEGER NOT NULL,
	"tag_id"	INTEGER NOT NULL,
	FOREIGN KEY("tag_group_id") REFERENCES "taggroups"("id"),
FOREIGN KEY("tag_id") REFERENCES "tags"("id")
)

CREATE TABLE taggroups
  (id            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
name	TEXT NOT NULL UNIQUE,
   plcid       INTEGER,
   machineid INTEGER,
   collection_method         INTEGER,
   collection_type       TEXT,

   FOREIGN KEY(plcid)       REFERENCES controller(id),
   FOREIGN KEY(machineid) REFERENCES machine(id)
)

CREATE TABLE "tags" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"register_typeid"	INTEGER,
	"address"	INTEGER,
	"scaling"	INTEGER,
	"data_type"	INTEGER,
	"data_size"	INTEGER,
	FOREIGN KEY("register_typeid") REFERENCES "register_types"("id")
)