#ifndef TAGGROUPCONFIG_H
#define TAGGROUPCONFIG_H

#include "TagConfig.h"
#include <string>
using namespace std;

class TagGroupConfig
{
    public:
        TagGroupConfig();
        virtual ~TagGroupConfig();

        string  TagGroupID;
        string  TagGroupName;
        int CollectionMethod;
        string CollectionType;
        string PLCName;
        string PLCDescription;
        int SlaveID;
        string ConnectionString;
        string DriverName;
        string DriverFormat;

        TagConfig* TagConfigCollection;
    protected:

    private:
};

#endif // TAGGROUPCONFIG_H
