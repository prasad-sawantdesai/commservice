#ifndef TAGGROUPCONFIG_H
#define TAGGROUPCONFIG_H
#include <vector>
#include "TagConfig.h"
#include <string>
using namespace std;

class TagGroupConfig
{
    public:
        TagGroupConfig();
        virtual ~TagGroupConfig();

        int  TagGroupID;
        string  TagGroupName;
        int CollectionMethod;
        string CollectionType;
        string PLCName;
        string PLCDescription;
        int SlaveID;
        string ConnectionString;
        string DriverName;
        string DriverFormat;

        vector<TagConfig> TagConfigCollection;
    protected:

    private:
};

#endif // TAGGROUPCONFIG_H
