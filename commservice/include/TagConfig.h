#ifndef TAGCONFIG_H
#define TAGCONFIG_H
#include <string>
using namespace std;

class TagConfig
{
public:
    TagConfig();
    virtual ~TagConfig();

    int  TagID;
    string TagName;
    string TagRegisterType;
    int RangeUpper;
    int RangeLower;
    int TagAddress;
    int TagScaling;
    int TagDataType;
    int TagDataSize;

protected:

private:
};

#endif // TAGCONFIG_H
