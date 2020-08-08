#ifndef SYSTEMSETTINGS_H
#define SYSTEMSETTINGS_H
#include <string>
using namespace std;

class SystemSettings
{
    public:
        SystemSettings();
        virtual ~SystemSettings();

        string MongoDBServerAddress;
    protected:

    private:
};

#endif // SYSTEMSETTINGS_H
