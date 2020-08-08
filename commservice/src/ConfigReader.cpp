#include "ConfigReader.h"
#include <stdio.h>
#include <sqlite3.h>
#include <string>
#include <sstream>
#include <vector>
#include <iostream>
#include "TagGroupConfig.h"
#include "SystemSettings.h"
using namespace std;
ConfigReader::ConfigReader()
{
    //ctor
}

ConfigReader::~ConfigReader()
{
    //dtor
}

vector<TagGroupConfig> ConfigReader::ReadConfiguration(string database_path)
{
    vector<TagGroupConfig> TagGroupConfigCollection;
    sqlite3 *db;
    sqlite3_stmt * RESTagGroup;
    sqlite3_stmt * RESTag;

    int rc, rcTag;

    rc = sqlite3_open(database_path.c_str(), &db);
    if( rc )
    {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return TagGroupConfigCollection;
    }
    string sqlTagGroupConfig = "SELECT taggroups.id AS 'TagGroupID', taggroups.name AS 'TagGroupName', taggroups.collection_method AS 'CollectionMethod',taggroups.collection_type AS 'CollectionType', \
                controller.name AS 'PLCName',controller.description AS 'PLCDescription', machine.manualid AS 'SlaveID', connection.connection_string AS 'ConnectionString', \
                driver.name AS 'DriverName', driver.format AS 'DriverFormat'\
                FROM ((((taggroups \
                INNER JOIN controller ON taggroups.plcid=controller.id) \
                INNER JOIN machine ON machine.plcid=controller.id) \
                INNER JOIN connection ON connection.plcid=controller.id) \
                INNER JOIN driver ON driver.id=connection.driverid) \
                ORDER BY controller.name, driver.name;";

    rc = sqlite3_prepare_v2(db,sqlTagGroupConfig.c_str(), -1, &RESTagGroup,0);

    if( rc != SQLITE_OK)
    {
        printf("\nFailed to get data: %s",sqlite3_errmsg(db));
        sqlite3_close(db);

        return TagGroupConfigCollection;
    }

    while (sqlite3_step(RESTagGroup) != SQLITE_DONE)
    {
        TagGroupConfig *objTagGroupConfig= new TagGroupConfig();
        objTagGroupConfig->TagGroupID = sqlite3_column_int(RESTagGroup,0);
        objTagGroupConfig->TagGroupName = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,1)));
        objTagGroupConfig->CollectionMethod = sqlite3_column_int(RESTagGroup,2);
        objTagGroupConfig->CollectionType = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,3)));
        objTagGroupConfig->PLCName = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,4)));
        objTagGroupConfig->PLCDescription = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,5)));
        objTagGroupConfig->SlaveID = sqlite3_column_int(RESTagGroup,6);
        objTagGroupConfig->ConnectionString = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,7)));
        objTagGroupConfig->DriverName = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,8)));
        objTagGroupConfig->DriverFormat = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,9)));
        objTagGroupConfig->ConnectionStatus = -1;


        string sqlTagConfig = "SELECT tags.id AS 'TagID', tags.name AS 'TagName',register_types.ragister_type AS 'TagRegisterType',\
register_types.range_upper AS 'RangeUpper',register_types.range_lower AS 'RangeLower',tags.address AS 'TagAddress',tags.scaling AS 'TagScaling',tags.data_type AS 'TagDataType',\
                tags.data_size AS 'TagDataSize' FROM tags, tag_group_mapping, taggroups, register_types\
				WHERE tag_group_mapping.tag_id=tags.id and tag_group_mapping.tag_group_id=taggroups.id and tags.register_typeid=register_types.id\
				and taggroups.id=";
		sqlTagConfig = sqlTagConfig + std::to_string(objTagGroupConfig->TagGroupID);
        vector<TagConfig> TagConfigCollectionObjects;

        rcTag = sqlite3_prepare_v2(db,sqlTagConfig.c_str(), -1, &RESTag,0);
        if( rcTag == SQLITE_OK)
        {
            while (sqlite3_step(RESTag) != SQLITE_DONE)
            {

                TagConfig *objTagConfig= new TagConfig();
                objTagConfig->TagID = sqlite3_column_int(RESTag,0);
                objTagConfig->TagName = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTag,1)));
                objTagConfig->TagRegisterType = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTag,2)));
                objTagConfig->RangeUpper = sqlite3_column_int(RESTag,3);
                objTagConfig->RangeLower = sqlite3_column_int(RESTag,4);
                objTagConfig->TagAddress = sqlite3_column_int(RESTag,5);
                objTagConfig->TagScaling = sqlite3_column_int(RESTag,6);
                objTagConfig->TagDataType = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTag,7)));
                objTagConfig->TagDataSize = sqlite3_column_int(RESTag,8);
                TagConfigCollectionObjects.push_back(*objTagConfig);
            }
        }
        objTagGroupConfig->TagConfigCollection = TagConfigCollectionObjects;
        TagGroupConfigCollection.push_back(*objTagGroupConfig);
    }



    sqlite3_finalize(RESTagGroup);
    sqlite3_close(db);

    return TagGroupConfigCollection;
}

SystemSettings ConfigReader::ReadSystemSettings(string database_path)
{
    SystemSettings objSystemSettings;
    sqlite3 *db;
    sqlite3_stmt * RESSystemSettings;

    int rc;

    rc = sqlite3_open(database_path.c_str(), &db);
    if( rc )
    {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return objSystemSettings;
    }

    string sqlSystemSettings = "SELECT * FROM SystemSettings";

    rc = sqlite3_prepare_v2(db,sqlSystemSettings.c_str(), -1, &RESSystemSettings,0);

    if( rc != SQLITE_OK)
    {
        printf("\nFailed to get data: %s",sqlite3_errmsg(db));
        sqlite3_close(db);

        return objSystemSettings;
    }

    while (sqlite3_step(RESSystemSettings) != SQLITE_DONE)
    {
        objSystemSettings= SystemSettings();
        objSystemSettings.MongoDBServerAddress = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESSystemSettings,0)));

    }

    sqlite3_finalize(RESSystemSettings);
    sqlite3_close(db);

    return objSystemSettings;
}

