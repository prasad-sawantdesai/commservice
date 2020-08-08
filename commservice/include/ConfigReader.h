#ifndef CONFIGREADER_H
#define CONFIGREADER_H
#include "TagGroupConfig.h"
#include "SystemSettings.h"
#include <string>
using namespace std;
class ConfigReader
{
    public:
        /** Default constructor */
        ConfigReader();
        /** Default destructor */
        virtual ~ConfigReader();
        vector<TagGroupConfig> ReadConfiguration(string);
        SystemSettings ReadSystemSettings(string);

    protected:

    private:
};

#endif // CONFIGREADER_H
