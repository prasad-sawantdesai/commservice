#include <iostream>
#include <cstdlib>
#include <pthread.h>
#include <time.h>
#include <cstdlib>
#include <vector>
#include <string>
#include <thread>
#include <unistd.h>

#include "ConfigReader.h"
#include "DatabaseWriter.h"
#include "TagGroupConfig.h"
#include "LibModbusClient.h"

using namespace std;

#define NUM_THREADS 1

const vector<string> split(const string& s, const char& c)
{
    string buff{""};
    vector<string> v;

    for(auto n:s)
    {
        if(n != c) buff+=n;
        else if(n == c && buff != "")
        {
            v.push_back(buff);
            buff = "";
        }
    }
    if(buff != "") v.push_back(buff);

    return v;
}

int main (int argc, char* argv[])
{
    if (argc < 2) {
        cout<<"Please provide database configuration file"<< std::endl;
        return 1;
    }
    string database_path = argv[1];

    //Read configuration database
    vector<TagGroupConfig>::iterator TagGroupConfigIterator;
    vector<TagConfig>::iterator TagConfigIterator;
    vector<TagGroupConfig> TagGroupConfigCollection;

    SystemSettings objSystemSettings;
    ConfigReader objConfigReader = ConfigReader();
    DatabaseWriter objDatabaseWriter = DatabaseWriter();
//"/home/ujjaini/prasad/commservice/git_repo/commservice/database/commservice_example.db" //
    TagGroupConfigCollection = objConfigReader.ReadConfiguration(database_path.c_str());
    objSystemSettings = objConfigReader.ReadSystemSettings(database_path.c_str());
    cout<<"---------Reading system settings----------"<< endl ;
    cout<<"MongoDB Address"<<objSystemSettings.MongoDBServerAddress<<endl<<endl;
    cout<<"---------Reading tag group configuration----------"<< endl ;

    for (TagGroupConfigIterator = TagGroupConfigCollection.begin(); TagGroupConfigIterator != TagGroupConfigCollection.end(); ++TagGroupConfigIterator)
    {
        cout <<"TagGroupID :"<< TagGroupConfigIterator->TagGroupID<< endl ;
        cout <<"TagGroupName :"<< TagGroupConfigIterator->TagGroupName<< endl ;
        cout <<"CollectionMethod :"<< TagGroupConfigIterator->CollectionMethod<< endl ;
        cout <<"CollectionType :"<< TagGroupConfigIterator->CollectionType<< endl ;
        cout <<"PLCName :"<< TagGroupConfigIterator->PLCName<< endl ;
        cout <<"PLCDescription :"<< TagGroupConfigIterator->PLCDescription<< endl ;
        cout <<"SlaveID :"<< TagGroupConfigIterator->SlaveID<< endl ;
        cout <<"ConnectionString :"<< TagGroupConfigIterator->ConnectionString<< endl ;
        cout <<"DriverName :"<< TagGroupConfigIterator->DriverName<< endl ;
        cout <<"DriverFormat :"<< TagGroupConfigIterator->DriverFormat<< endl ;
        cout << "Tags available in the group:" << endl ;

        for (TagConfigIterator = TagGroupConfigIterator->TagConfigCollection.begin(); TagConfigIterator != TagGroupConfigIterator->TagConfigCollection.end(); ++TagConfigIterator)
        {

            cout <<"\tTagID :"<< TagConfigIterator->TagID<< endl ;
            cout <<"\tTagName :"<< TagConfigIterator->TagName<< endl ;
            cout <<"\tTagRegisterType :"<< TagConfigIterator->TagRegisterType<< endl ;
            cout <<"\tRangeUpper :"<< TagConfigIterator->RangeUpper<< endl ;
            cout <<"\tRangeLower :"<< TagConfigIterator->RangeLower<< endl ;
            cout <<"\tTagAddress :"<< TagConfigIterator->TagAddress<< endl ;
            cout <<"\tTagScaling :"<< TagConfigIterator->TagScaling<< endl ;
            cout <<"\tTagDataType :"<< TagConfigIterator->TagDataType<< endl ;
            cout <<"\tTagDataSize :"<< TagConfigIterator->TagDataSize<< endl ;
            cout<<"\t-----------------------------"<< endl ;
        }
        cout<<"------------------------------------"<< endl ;
    }
    //Setup connection
    for (TagGroupConfigIterator = TagGroupConfigCollection.begin(); TagGroupConfigIterator != TagGroupConfigCollection.end(); ++TagGroupConfigIterator)
    {

        if (TagGroupConfigIterator->DriverName.compare("Modbus TCP") ==0)
        {
            //IPADDRESS:192.168.1.100;PORT:502
            cout<<"----------------------------------------------------------------------"<<endl;
            vector<string> splitted_connectionstring{split(TagGroupConfigIterator->ConnectionString, ';')};
            vector<string> ipaddress{split(splitted_connectionstring[0], ':')};
            vector<string> port{split(splitted_connectionstring[1], ':')};

            TagGroupConfigIterator->objLibModbusClient= TagGroupConfigIterator->objLibModbusClient.CreateTcpClient(ipaddress[1].c_str(),atoi(port[1].c_str()));

            TagGroupConfigIterator->ConnectionStatus = TagGroupConfigIterator->objLibModbusClient.connect();
            if (TagGroupConfigIterator->ConnectionStatus == 0)
                cout<<"Connected Successfully to "<<TagGroupConfigIterator->ConnectionString<<endl;
            else
                cout<<"Connection issue "<<TagGroupConfigIterator->ConnectionString<<endl;
        }
        if (TagGroupConfigIterator->DriverName.compare("Modbus RTU") ==0)
        {
            //COMPORT:COM3;BAUDRATE:19200;PARITY:NONE;BYTESIZE:8;STOPBITS:1
            //"/dev/ttyUSB0",19200, 'N', 8, 1
            vector<string> splitted_connectionstring{split(TagGroupConfigIterator->ConnectionString, ';')};
            vector<string> comport{split(splitted_connectionstring[0], ':')};
            vector<string> baudrate{split(splitted_connectionstring[1], ':')};
            vector<string> parity{split(splitted_connectionstring[2], ':')};
            vector<string> byte_size{split(splitted_connectionstring[3], ':')};
            vector<string> stop_bits{split(splitted_connectionstring[4], ':')};

            //TagGroupConfigIterator->objLibModbusClient= TagGroupConfigIterator->objLibModbusClient.CreateRtuClient("/dev/ttyUSB0",9600, 'N', 8, 1);
            TagGroupConfigIterator->objLibModbusClient= TagGroupConfigIterator->objLibModbusClient.CreateRtuClient(comport[1].c_str(),atoi(baudrate[1].c_str()),'N',atoi(byte_size[1].c_str()),atoi(stop_bits[1].c_str()));
            TagGroupConfigIterator->objLibModbusClient.SetSlaveID(99);
            TagGroupConfigIterator->ConnectionStatus = TagGroupConfigIterator->objLibModbusClient.connect();
            if (TagGroupConfigIterator->ConnectionStatus == 0)
                cout<<"Connected Successfully to "<<TagGroupConfigIterator->ConnectionString<<endl;
            else
                cout<<"Connection issue "<<TagGroupConfigIterator->ConnectionString<<endl;
        }
    }

    //Read data from active connection
    while(1)
    {

        for (TagGroupConfigIterator = TagGroupConfigCollection.begin(); TagGroupConfigIterator != TagGroupConfigCollection.end(); ++TagGroupConfigIterator)
        {

            if (TagGroupConfigIterator->DriverName.compare("Modbus TCP") ==0)
            {
                //IPADDRESS:192.168.1.100;PORT:502
                if (TagGroupConfigIterator->ConnectionStatus !=0)
                {
                    cout<<"----------------------------------------------------------------------"<<endl;
                    vector<string> splitted_connectionstring{split(TagGroupConfigIterator->ConnectionString, ';')};
                    vector<string> ipaddress{split(splitted_connectionstring[0], ':')};
                    vector<string> port{split(splitted_connectionstring[1], ':')};

                    TagGroupConfigIterator->objLibModbusClient= TagGroupConfigIterator->objLibModbusClient.CreateTcpClient(ipaddress[1].c_str(),atoi(port[1].c_str()));


                    TagGroupConfigIterator->ConnectionStatus = TagGroupConfigIterator->objLibModbusClient.connect();
                    if (TagGroupConfigIterator->ConnectionStatus == 0)
                        cout<<"Connected Successfully to "<<TagGroupConfigIterator->ConnectionString<<endl;
                    else
                        cout<<"Connection issue with "<<TagGroupConfigIterator->ConnectionString<<endl;
                }
            }
            if (TagGroupConfigIterator->DriverName.compare("Modbus RTU") ==0)
            {
                if (TagGroupConfigIterator->ConnectionStatus !=0)
                {
                    vector<string> splitted_connectionstring{split(TagGroupConfigIterator->ConnectionString, ';')};
                    vector<string> comport{split(splitted_connectionstring[0], ':')};
                    vector<string> baudrate{split(splitted_connectionstring[1], ':')};
                    vector<string> parity{split(splitted_connectionstring[2], ':')};
                    vector<string> byte_size{split(splitted_connectionstring[3], ':')};
                    vector<string> stop_bits{split(splitted_connectionstring[4], ':')};

                    TagGroupConfigIterator->objLibModbusClient= TagGroupConfigIterator->objLibModbusClient.CreateRtuClient("/dev/ttyUSB0",9600, 'N', 8, 1);
                    //TagGroupConfigIterator->objLibModbusClient= TagGroupConfigIterator->objLibModbusClient.CreateRtuClient(comport[1].c_str(),atoi(baudrate[1].c_str()),'N',atoi(byte_size[1].c_str()),atoi(stop_bits[1].c_str()));

                    TagGroupConfigIterator->ConnectionStatus = TagGroupConfigIterator->objLibModbusClient.connect();
                    if (TagGroupConfigIterator->ConnectionStatus == 0)
                        cout<<"Connected Successfully to "<<TagGroupConfigIterator->ConnectionString<<endl;
                    else
                        cout<<"Connection issue "<<TagGroupConfigIterator->ConnectionString<<endl;
                }

            }
            if (TagGroupConfigIterator->ConnectionStatus  ==0)
            {
                for (TagConfigIterator = TagGroupConfigIterator->TagConfigCollection.begin(); TagConfigIterator != TagGroupConfigIterator->TagConfigCollection.end(); ++TagConfigIterator)
                {
                    cout <<TagGroupConfigIterator->TagGroupName<<":"<<TagConfigIterator->TagName<< " from address "<<TagConfigIterator->TagAddress<<" , " << TagGroupConfigIterator->PLCName << " using " << TagGroupConfigIterator->DriverName<< " ["<<TagGroupConfigIterator->ConnectionString <<"] "<<endl ;

                    time_t current_time = time(NULL);
                    bson_t *doc;
                    bson_oid_t oid;
                    doc = bson_new ();
                    bson_oid_init (&oid, NULL);
                    BSON_APPEND_OID (doc, "_id", &oid);
                    BSON_APPEND_UTF8 (doc, "Time", ctime(&current_time));
                    BSON_APPEND_UTF8 (doc, "TagGroupName", TagGroupConfigIterator->TagGroupName.c_str());
                    BSON_APPEND_UTF8 (doc, "TagName", TagConfigIterator->TagName.c_str());

                    BSON_APPEND_UTF8 (doc, "PLCName", TagGroupConfigIterator->PLCName.c_str());
                    BSON_APPEND_UTF8 (doc, "Protocol", TagGroupConfigIterator->DriverName.c_str());
                    BSON_APPEND_UTF8 (doc, "ConnectionString", TagGroupConfigIterator->ConnectionString.c_str());
                    BSON_APPEND_INT32 (doc, "SlaveID", TagGroupConfigIterator->SlaveID);
                    BSON_APPEND_INT32 (doc, "TagAddress", TagConfigIterator->TagAddress);
                    if (TagConfigIterator->TagRegisterType.compare("Holding registers") ==0)
                    {
                        uint16_t* holding_reg = TagGroupConfigIterator->objLibModbusClient.ReadHoldingRegisters(TagConfigIterator->TagAddress, TagConfigIterator->TagDataSize);
                        if(holding_reg!=NULL)
                        {
                            //data types : float32, float64, int16, int32, uint16, uint32, bits
                            if(TagConfigIterator->TagDataType.compare("float32") ==0)
                            {
                                cout<<"Raw values :"<<holding_reg[0]<<" "<<holding_reg[1]<<" "<<holding_reg[2]<<" "<<holding_reg[3]<<endl;
                                BSON_APPEND_DOUBLE (doc, "Value", modbus_get_float_cdab(holding_reg));
                                //cout<<"Converted value "<<modbus_get_float_abcd(holding_reg)<<endl;
                                //cout<<"Converted value "<<modbus_get_float_badc(holding_reg)<<endl;
                                cout<<"Converted value "<<modbus_get_float_cdab(holding_reg)<<endl;
                                //cout<<"Converted value "<<modbus_get_float_dcba(holding_reg)<<endl;
                                BSON_APPEND_BOOL (doc, "Connected", true);
                            }
                            if(TagConfigIterator->TagDataType.compare("int16") ==0)
                            {
                                cout<<"Raw values :"<<holding_reg[0]<<endl;
                                BSON_APPEND_DOUBLE (doc, "Value", (int)holding_reg[0]);
                                cout<<"Converted value "<<(int)holding_reg[0]<<endl;
                                BSON_APPEND_BOOL (doc, "Connected", true);
                            }
                            if(TagConfigIterator->TagDataType.compare("int32") ==0)
                            {
                                cout<<"Raw values :"<<holding_reg[0]<<holding_reg[1]<<endl;
                                uint32_t uint32 = holding_reg[0];
                                uint32 <<= 16;
                                uint32 |= holding_reg[1];
                                int32_t sint32 = (int32_t)uint32;
                                BSON_APPEND_INT32 (doc, "Value", sint32);
                                cout<<"Converted value "<<sint32<<endl;
                                BSON_APPEND_BOOL (doc, "Connected", true);
                            }
                        }
                        else
                        {
                            BSON_APPEND_INT32 (doc, "Value", 0);
                            BSON_APPEND_BOOL(doc, "Connected", false);
                        }
                    }
                    if (TagConfigIterator->TagRegisterType.compare("Input Registers") ==0)
                    {
                        uint16_t* input_reg = TagGroupConfigIterator->objLibModbusClient.ReadInputRegisters(TagConfigIterator->TagAddress, TagConfigIterator->TagDataSize);
                        if(input_reg!=NULL)
                        {
                            //data types : float32, float64, int16, int32, uint16, uint32, bits
                            if(TagConfigIterator->TagDataType.compare("float32") ==0)
                            {
                                cout<<"Raw values :"<<input_reg[0]<<" "<<input_reg[1]<<" "<<input_reg[2]<<" "<<input_reg[3]<<endl;
                                BSON_APPEND_DOUBLE (doc, "Value", modbus_get_float_cdab(input_reg));
                                //cout<<"Converted value "<<modbus_get_float_abcd(holding_reg)<<endl;
                                //cout<<"Converted value "<<modbus_get_float_badc(holding_reg)<<endl;
                                cout<<"Converted value "<<modbus_get_float_cdab(input_reg)<<endl;
                                //cout<<"Converted value "<<modbus_get_float_dcba(holding_reg)<<endl;
                                BSON_APPEND_BOOL (doc, "Connected", true);
                            }
                            if(TagConfigIterator->TagDataType.compare("int16") ==0)
                            {
                                cout<<"Raw values :"<<input_reg[0]<<endl;
                                BSON_APPEND_DOUBLE (doc, "Value", (int)input_reg[0]);
                                cout<<"Converted value "<<(int)input_reg[0]<<endl;
                                BSON_APPEND_BOOL (doc, "Connected", true);
                            }
                            if(TagConfigIterator->TagDataType.compare("int32") ==0)
                            {
                                cout<<"Raw values :"<<input_reg[0]<<input_reg[1]<<endl;
                                uint32_t uint32 = input_reg[0];
                                uint32 <<= 16;
                                uint32 |= input_reg[1];
                                int32_t sint32 = (int32_t)uint32;
                                BSON_APPEND_INT32 (doc, "Value", sint32);
                                cout<<"Converted value "<<sint32<<endl;
                                BSON_APPEND_BOOL (doc, "Connected", true);
                            }
                        }
                        else
                        {
                            BSON_APPEND_INT32 (doc, "Value", 0);
                            BSON_APPEND_BOOL(doc, "Connected", false);
                        }

                    }
                    if (TagConfigIterator->TagRegisterType.compare("Output coils") ==0)
                    {
                        uint8_t* coil = TagGroupConfigIterator->objLibModbusClient.ReadOutputCoils(TagConfigIterator->TagAddress, TagConfigIterator->TagDataSize);

                        if(coil!=NULL)
                        {
                            cout<<"Raw value :"<< unsigned(coil[0])<<endl;
                            if(coil[0] == 1)
                                BSON_APPEND_BOOL (doc, "Value", true);
                            else
                                BSON_APPEND_BOOL (doc, "Value", false);
                            BSON_APPEND_BOOL (doc, "Connected", true);
                        }
                        else
                        {
                            BSON_APPEND_BOOL (doc, "Value", false);
                            BSON_APPEND_BOOL (doc, "Connected", false);
                        }
                    }
                    if (TagConfigIterator->TagRegisterType.compare("Discrete inputs") ==0)
                    {
                        uint8_t* discrete_input = TagGroupConfigIterator->objLibModbusClient.ReadDiscreteInputs(TagConfigIterator->TagAddress, TagConfigIterator->TagDataSize);

                        if(discrete_input!=NULL)
                        {
                            cout<<"Raw value :"<<unsigned(discrete_input[0])<<endl;
                            if(discrete_input[0] == 1)
                                BSON_APPEND_BOOL (doc, "Value", true);
                            else
                                BSON_APPEND_BOOL (doc, "Value", false);

                            BSON_APPEND_BOOL (doc, "Connected", true);
                        }
                        else
                        {
                            BSON_APPEND_BOOL (doc, "Value", false);
                            BSON_APPEND_BOOL (doc, "Connected", false);
                        }
                    }
                    //objDatabaseWriter.upload_data("mongodb://localhost:27017", doc);
                    objDatabaseWriter.upload_data(objSystemSettings.MongoDBServerAddress, doc);
                    if (TagGroupConfigIterator->DriverName.compare("Modbus RTU") ==0)
                    {
                        sleep(1);
                    }
                }
                sleep(TagGroupConfigIterator->CollectionMethod);

            }

        }

    }
    //Close all connections
    for (TagGroupConfigIterator = TagGroupConfigCollection.begin(); TagGroupConfigIterator != TagGroupConfigCollection.end(); ++TagGroupConfigIterator)
    {

        TagGroupConfigIterator->objLibModbusClient.close();
    }
}

//------------------------------------------END----------------------------

void func_dummy(int N )
{
    for (int i = 0; i < N; i++)
    {
        cout << "Thread 1 :: callable => function pointer\n";
    }
    LibModbusClient obj;

    obj= obj.CreateRtuClient("/dev/ttyUSB0",19200, 'N', 8, 1);
    if (obj.mb != NULL)
    {
        obj.SetSlaveID(99);
        obj.connect();
        uint16_t* holding_reg = obj.ReadHoldingRegisters(5, 10);

        for (int i=0; i < 5; i++)
        {
            printf("holding register[%d]=%d (0x%X)\n",i, holding_reg[i], holding_reg[i]);
        }
        obj.close();
    }
}
void *modbusrtu(void *slaveid)
{
    int sid = (long)slaveid;
    cout<<"Modbus client is connecting to :"<<sid<<endl;

    LibModbusClient obj;

    obj= obj.CreateRtuClient("/dev/ttyUSB0",19200, 'N', 8, 1);

    obj.SetSlaveID(99);
    obj.connect();

//    timeval curTime;
//gettimeofday(&curTime, NULL);
//int milli = curTime.tv_usec / 1000;
//
//char buffer [80];
//strftime(buffer, 80, "%Y-%m-%d %H:%M:%S", localtime(&curTime.tv_sec));
//
//char currentTime[84] = "";
//sprintf(currentTime, "%s:%03d", buffer, milli);
//printf("current time: %s \n", currentTime);

    time_t my_time = time(NULL);
    uint16_t* holding_reg = obj.ReadHoldingRegisters(5, 10);


    for (int i=0; i < 5; i++)
    {

        printf("%s :holding register[%d]=%d (0x%X)\n",ctime(&my_time),i, holding_reg[i], holding_reg[i]);
    }

    uint16_t* input_reg = obj.ReadInputRegisters(5, 10);

    for (int i=0; i < 5; i++)
    {
        printf("%s :input register[%d]=%d (0x%X)\n",ctime(&my_time),i, input_reg[i], input_reg[i]);
    }

//    uint8_t* input_coils = obj.ReadInputCoils(0, 2);
//
//    for (int i=0; i < 5; i++)
//    {
//        printf("%s :input coils[%d]=%d (0x%X)\n",ctime(&my_time),i, input_coils[i], input_coils[i]);
//    }
    obj.close();
    return 0;
}
struct structModbusTCP
{
    const char* ip_address;
    int port;
    int slaveid;
};
void *modbustcp(void *input)
{
    const char* ip_address;
    int port;
    int slaveid;
    ip_address = ((struct structModbusTCP*)input)->ip_address;
    port = ((struct structModbusTCP*)input)->port;
    slaveid = ((struct structModbusTCP*)input)->slaveid;

    cout<<"Modbus client is connecting to :"<<slaveid<<endl;

    LibModbusClient obj;

    obj= obj.CreateTcpClient(ip_address,port);
    obj.SetSlaveID(slaveid);
    obj.connect();

//    timeval curTime;
//gettimeofday(&curTime, NULL);
//int milli = curTime.tv_usec / 1000;
//
//char buffer [80];
//strftime(buffer, 80, "%Y-%m-%d %H:%M:%S", localtime(&curTime.tv_sec));
//
//char currentTime[84] = "";
//sprintf(currentTime, "%s:%03d", buffer, milli);
//printf("current time: %s \n", currentTime);

//TagName
//TagGroup
//PLC
//Protocol
//IPAddress
//Port
//COM
//Slave ID
//RawValue
//Value

    time_t my_time = time(NULL);
    uint16_t* holding_reg = obj.ReadHoldingRegisters(0, 20);
//    const char * sample_tag = "sampletag";
    for (int i=0; i < 5; i++)
    {
//        DatabaseWriter objDatabaseWriter = DatabaseWriter();
//        objDatabaseWriter.upload_data("mongodb://localhost:27017", sample_tag, holding_reg[i]);
        printf("%s :holding register[%d]=%d (0x%X)\n",ctime(&my_time),i, holding_reg[i], holding_reg[i]);
    }

    uint16_t* input_reg = obj.ReadInputRegisters(0, 20);

    for (int i=0; i < 5; i++)
    {
        printf("%s :input register[%d]=%d (0x%X)\n",ctime(&my_time),i, input_reg[i], input_reg[i]);
    }

//    uint8_t* input_coils = obj.ReadInputCoils(0, 2);
//
//    for (int i=0; i < 5; i++)
//    {
//        printf("%s :input coils[%d]=%d (0x%X)\n",ctime(&my_time),i, input_coils[i], input_coils[i]);
//    }
    obj.close();
    return 0;
}


//connect to mongo db



//    for( i = 0; i < NUM_THREADS; i++ )
//    {
//        cout << "\nmain() : creating tcp modbus connection thread, " << i << endl;
//        int rc = pthread_create(&threads[i], NULL, modbustcp, (void *)i);
//
//        //cout << "\nmain() : creating rtu modbus connection thread, " << i << endl;
//        //rc = pthread_create(&threads[i], NULL, modbusrtu, (void *)i);
//
//        if (rc)
//        {
//            cout << "\n Error:unable to create thread," << rc << endl;
//            exit(-1);
//        }
//    }
//    pthread_exit(NULL);
//}

//    int *array = new int[number];
//
//    for (int i=0; i < rc; i++)
//    {
//        printf("reg[%d]=%d (0x%X)\n", i, tab_reg[i], tab_reg[i]);
//        array[i] = (int)tab_reg[i];
//        cout<<array[i];
//    }
//    return array;
//     for (int i = 0; i < 4; i++ ) {
//      printf( "*(array + %d) : (0x%X)\n", i, *(array + i));
//   }
//    int rc=5;
//        for (int i=0; i < rc; i++)
//    {
//        printf("reg[%d]=%d (0x%X)\n", i, array[i], array[i]);
//    }
/* Read 5 registers from the address 0 */
//modbus_read_registers(mb, 0, 5, tab_reg);
//    for (int i=0; i < rc; i++)
//    {
//        printf("%s : reg[%d]=%d (0x%X)\n", ctime(&my_time), i, tab_reg[i], tab_reg[i]);
//    }

//struct structModbusTCP *modbusTCPConfig = (struct structModbusTCP *)malloc(sizeof(struct structModbusTCP));
//                    vector<string> v{split(TagGroupConfigIterator->ConnectionString, ';')};
//                    vector<string> v1{split(v[0], ':')};
//                    vector<string> v2{split(v[1], ':')};
//
//                    modbusTCPConfig->ip_address = v1[1].c_str();
//                    modbusTCPConfig->port = atoi(v2[1].c_str());
//                    modbusTCPConfig->slaveid = TagGroupConfigIterator->SlaveID;
//                    std::thread th1(func_dummy, 2);
//                    th1.join();
//-------------------------------------------
//COMPORT:COM3;BAUDRATE:19200;PARITY:NONE;BYTESIZE:8;STOPBITS:1
//"/dev/ttyUSB0",19200, 'N', 8, 1
//                vector<string> splitted_connectionstring{split(TagGroupConfigIterator->ConnectionString, ';')};
//                vector<string> comport{split(splitted_connectionstring[0], ':')};
//                vector<string> baudrate{split(splitted_connectionstring[1], ':')};
//                vector<string> parity{split(splitted_connectionstring[2], ':')};
//                vector<string> byte_size{split(splitted_connectionstring[3], ':')};
//                vector<string> stop_bits{split(splitted_connectionstring[4], ':')};
//                LibModbusClient obj1;
//                obj1= obj1.CreateRtuClient("/dev/ttyUSB0",19200, 'N', 8, 1);
////                obj= obj.CreateRtuClient(comport[1].c_str(),atoi(baudrate[1].c_str()),'N',atoi(byte_size[1].c_str()),atoi(stop_bits[1].c_str()));
//                obj1.SetSlaveID(99);
//                obj1.connect();
//                uint16_t* holding_reg = obj1.ReadHoldingRegisters(5, 10);
//
//
//                for (int i=0; i < 5; i++)
//                {
//
//                    printf("holding register[%d]=%d (0x%X)\n",i, holding_reg[i], holding_reg[i]);
//                }
//int connection_success =0;
//
//                if (connection_success ==0)
//                {
//                    for (TagConfigIterator = TagGroupConfigIterator->TagConfigCollection.begin(); TagConfigIterator != TagGroupConfigIterator->TagConfigCollection.end(); ++TagConfigIterator)
//                    {
//                        cout <<"Reading tag :"<< TagConfigIterator->TagName<< " from "<< TagGroupConfigIterator->PLCName << " using " << TagGroupConfigIterator->DriverName<< " ["<<TagGroupConfigIterator->ConnectionString <<"] "<< endl ;
//                        if (TagConfigIterator->TagRegisterType.compare("Holding registers") ==0)
//                        {
//                            uint16_t* holding_reg1 = obj1.ReadHoldingRegisters(5, 10);
//                            cout<<"Value read :"<<holding_reg1[0]<<endl;
//                        }
//                        if (TagConfigIterator->TagRegisterType.compare("Input Registers") ==0)
//                        {
//                            uint16_t* input_reg = obj1.ReadInputRegisters(TagConfigIterator->TagAddress, 1);
//                            cout<<"Value read :"<<input_reg[0]<<endl;
//                        }
//                        if (TagConfigIterator->TagRegisterType.compare("Output coils") ==0)
//                        {
//                            uint8_t* coil = obj1.ReadInputCoils(TagConfigIterator->TagAddress, 1);
//                            cout<<"Value read :"<<coil[0]<<endl;
//                        }
//                        if (TagConfigIterator->TagRegisterType.compare("Discrete inputs") ==0)
//                        {
//                            uint8_t* discrete_input = obj1.ReadInputCoils(TagConfigIterator->TagAddress, 1);
//                            cout<<"Value read :"<<discrete_input[0]<<endl;
//                        }
//                        sleep(1);
//                    }
//
//                }
//                obj1.close();
//                //if(connection_success ==0)
//
//            }
