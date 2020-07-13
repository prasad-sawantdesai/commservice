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

TagGroupConfig* ConfigReader::ReadConfiguration(string database_path)
{
    sqlite3 *db;
    sqlite3_stmt * RESTagGroup;
    sqlite3_stmt * RESTag;
    char *err_msg = 0;

    int rc, rcTag;

    rc = sqlite3_open(database_path.c_str(), &db);
    if( rc )
    {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return NULL;
    }
    else
    {
        fprintf(stderr, "Opened database successfully\n");
    }

    char *sqlTagGroupConfig = "SELECT taggroups.id AS 'TagGroupID', taggroups.name AS 'TagGroupName', taggroups.collection_method AS 'CollectionMethod',taggroups.collection_type AS 'CollectionType', \
                controller.name AS 'PLCName',controller.description AS 'PLCDescription', machine.manualid AS 'SlaveID', connection.connection_string AS 'ConnectionString', \
                driver.name AS 'DriverName', driver.format AS 'DriverFormat'\
                FROM ((((taggroups \
                INNER JOIN controller ON taggroups.plcid=controller.id) \
                INNER JOIN machine ON machine.plcid=controller.id) \
                INNER JOIN connection ON connection.plcid=controller.id) \
                INNER JOIN driver ON driver.id=connection.driverid) \
                ORDER BY controller.name, driver.name;";

    char *sqlTagConfig = "SELECT tags.id AS 'TagID', tags.name AS 'TagName',\
                register_types.ragister_type AS 'TagRegisterType',register_types.range_upper AS 'RangeUpper',\
                register_types.range_lower AS 'RangeLower',tags.address AS 'TagAddress',\
                tags.scaling AS 'TagScaling',tags.data_type AS 'TagDataType',\
                tags.data_size AS 'TagDataSize' FROM (((tags \
                INNER JOIN tag_group_mapping ON tag_group_mapping.tag_id=tags.id) \
                INNER JOIN register_types ON tags.register_typeid=register_types.id) \
                INNER JOIN taggroups ON taggroups.id=tag_group_mapping.id) \
				where taggroups.id=1";
    rc = sqlite3_prepare_v2(db,sqlTagGroupConfig, -1, &RESTagGroup,0);

    if( rc != SQLITE_OK)
    {
        printf("\nFailed to get data: %s",sqlite3_errmsg(db));
        sqlite3_close(db);

        return NULL;
    }


    int size = 20;
    TagGroupConfig* TagGroupConfigCollection = new TagGroupConfig[size];

    int counter = 0;
    while (sqlite3_step(RESTagGroup) != SQLITE_DONE)
    {
        TagGroupConfig objTagGroupConfig= TagGroupConfig();
        objTagGroupConfig.TagGroupID = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,0)));
        objTagGroupConfig.TagGroupName = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,1)));
        objTagGroupConfig.CollectionMethod = sqlite3_column_int(RESTagGroup,2);
        objTagGroupConfig.CollectionType = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,3)));
        objTagGroupConfig.PLCName = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,4)));
        objTagGroupConfig.PLCDescription = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,5)));
        objTagGroupConfig.SlaveID = sqlite3_column_int(RESTagGroup,6);
        objTagGroupConfig.ConnectionString = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,7)));
        objTagGroupConfig.DriverName = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,8)));
        objTagGroupConfig.DriverFormat = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTagGroup,9)));


        TagConfig* objTagConfigCollection = new TagConfig[size];
        rcTag = sqlite3_prepare_v2(db,sqlTagConfig, -1, &RESTag,0);
        if( rcTag == SQLITE_OK)
        {
            int internalcounter = 0;
            while (sqlite3_step(RESTag) != SQLITE_DONE)
            {

                TagConfig objTagConfig= TagConfig();
                objTagConfig.TagID = sqlite3_column_int(RESTag,0);
                objTagConfig.TagName = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTag,1)));
                objTagConfig.TagRegisterType = std::string(reinterpret_cast<const char*>(sqlite3_column_text(RESTag,2)));
                objTagConfig.RangeUpper = sqlite3_column_int(RESTag,3);
                objTagConfig.RangeLower = sqlite3_column_int(RESTag,4);
                objTagConfig.TagAddress = sqlite3_column_int(RESTag,5);
                objTagConfig.TagScaling = sqlite3_column_int(RESTag,6);
                objTagConfig.TagDataType = sqlite3_column_int(RESTag,7);
                objTagConfig.TagDataSize = sqlite3_column_int(RESTag,8);

                objTagConfigCollection[internalcounter] = objTagConfig;
                internalcounter = internalcounter +1;
            }
        }
        objTagGroupConfig.TagConfigCollection = objTagConfigCollection;
        TagGroupConfigCollection[counter] = objTagGroupConfig;
        counter = counter +1;
    }

    sqlite3_finalize(RESTagGroup);
    sqlite3_close(db);

    return TagGroupConfigCollection;
}


