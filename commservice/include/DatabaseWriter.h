#ifndef DATABASEWRITER_H
#define DATABASEWRITER_H
#include <bson/bson.h>
#include <mongoc/mongoc.h>
#include <string>
using namespace std;

class DatabaseWriter
{
    public:
        DatabaseWriter();
        virtual ~DatabaseWriter();
        int upload_data(string, bson_t *);
    protected:

    private:
};

#endif // DATABASEWRITER_H
