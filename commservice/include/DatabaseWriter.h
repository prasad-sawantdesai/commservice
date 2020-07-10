#ifndef DATABASEWRITER_H
#define DATABASEWRITER_H
#include <string>
using namespace std;

class DatabaseWriter
{
    public:
        DatabaseWriter();
        virtual ~DatabaseWriter();
        int upload_data(string, const char *, int);
    protected:

    private:
};

#endif // DATABASEWRITER_H
