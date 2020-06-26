#include "ConfigReader.h"
#include <stdio.h>
#include <sqlite3.h>
#include <string>

using namespace std;
ConfigReader::ConfigReader()
{
    //ctor
}

ConfigReader::~ConfigReader()
{
    //dtor
}

int ConfigReader::Connect(string database_path)
{
   sqlite3 *db;
   //char *zErrMsg = 0;
   int rc;

   rc = sqlite3_open(database_path.c_str(), &db);

   if( rc ) {
      fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
      return(0);
   } else {
      fprintf(stderr, "Opened database successfully\n");
   }
   sqlite3_close(db);
    return 0;
}
