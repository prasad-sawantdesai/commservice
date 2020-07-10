#ifndef CONFIGREADER_H
#define CONFIGREADER_H
#include "TagGroupConfig.h"
#include <string>
using namespace std;
class ConfigReader
{
    public:
        /** Default constructor */
        ConfigReader();
        /** Default destructor */
        virtual ~ConfigReader();
        TagGroupConfig ReadConfiguration(string);

    protected:

    private:
};

#endif // CONFIGREADER_H
