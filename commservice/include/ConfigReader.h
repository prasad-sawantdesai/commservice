#ifndef CONFIGREADER_H
#define CONFIGREADER_H
#include <string>
using namespace std;
class ConfigReader
{
    public:
        /** Default constructor */
        ConfigReader();
        /** Default destructor */
        virtual ~ConfigReader();
        int Connect(string);
    protected:

    private:
};

#endif // CONFIGREADER_H
