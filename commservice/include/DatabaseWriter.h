#ifndef DATABASEWRITER_H
#define DATABASEWRITER_H
#include <string>
using namespace std;

class DatabaseWriter
{
    public:
        DatabaseWriter();
        virtual ~DatabaseWriter();
        int Connect(string);
    protected:

    private:
};

#endif // DATABASEWRITER_H
