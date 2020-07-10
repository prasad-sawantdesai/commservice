#include "ConfigReader.h"
#include <stdio.h>
#include <sqlite3.h>
#include <string.h>
#include <sstream>
#include "TagGroupConfig.h"
using namespace std;
ConfigReader::ConfigReader()
{
    //ctor
}

ConfigReader::~ConfigReader()
{
    //dtor
}

TagGroupConfig ConfigReader::ReadConfiguration(string database_path)
{
    sqlite3 *db;
    sqlite3_stmt * RES;
    char *err_msg = 0;
    TagGroupConfig objTagGroupConfig = TagGroupConfig();
    int rc;

    rc = sqlite3_open(database_path.c_str(), &db);
    if( rc )
    {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return objTagGroupConfig;
    }
    else
    {
        fprintf(stderr, "Opened database successfully\n");
    }

    char *sql = "SELECT taggroups.name AS 'TagGroupName', taggroups.collection_method AS 'CollectionMethod',taggroups.collection_type AS 'CollectionType', \
                controller.name AS 'PLCName',controller.description AS 'PLCDescription', machine.manualid AS 'SlaveID', connection.connection_string AS 'ConnectionString', \
                driver.name AS 'DriverName', driver.format AS 'DriverFormat'\
                FROM ((((taggroups \
                INNER JOIN controller ON taggroups.plcid=controller.id) \
                INNER JOIN machine ON machine.plcid=controller.id) \
                INNER JOIN connection ON connection.plcid=controller.id) \
                INNER JOIN driver ON driver.id=connection.driverid) \
                ORDER BY controller.name, driver.name;";

    rc = sqlite3_prepare_v2(db,sql, -1, &RES,0);

    if( rc != SQLITE_OK)
    {
        printf("\nFailed to get data: %s",sqlite3_errmsg(db));
        sqlite3_close(db);

        return objTagGroupConfig;
    }

    rc = sqlite3_step(RES);

    if(rc == SQLITE_ROW)
    {
        objTagGroupConfig.TagGroupName = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RES,0)));
        objTagGroupConfig.CollectionMethod = sqlite3_column_int(RES,1);
        objTagGroupConfig.CollectionType = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RES,2)));
        objTagGroupConfig.PLCName = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RES,3)));
        objTagGroupConfig.PLCDescription = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RES,4)));
        objTagGroupConfig.SlaveID = sqlite3_column_int(RES,5);
        objTagGroupConfig.ConnectionString = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RES,6)));
        objTagGroupConfig.DriverName = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RES,7)));
        objTagGroupConfig.DriverFormat = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RES,8)));
    }

    sqlite3_finalize(RES);
    sqlite3_close(db);

    return objTagGroupConfig;
}


