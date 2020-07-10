#include <iostream>
#include <cstdlib>
#include <pthread.h>
#include <time.h>
#include <cstdlib>
#include "ConfigReader.h"
#include "DatabaseWriter.h"
#include "TagGroupConfig.h"
#include "LibModbusClient.h"
#include <vector>
#include <string>
#include <unistd.h>
using namespace std;

#define NUM_THREADS 1
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
const char * sample_tag = "sampletag";
    for (int i=0; i < 5; i++)
    {
          DatabaseWriter objDatabaseWriter = DatabaseWriter();
        objDatabaseWriter.upload_data("mongodb://localhost:27017", sample_tag, holding_reg[i]);
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
int main ()
{
    //Read configuration database
    ConfigReader objConfigReader = ConfigReader();
    TagGroupConfig objTagGroupConfig = objConfigReader.ReadConfiguration("/home/ujjaini/prasad/commservice/git_repo/commservice/database/commservice_example.db");

    printf("%s\n",objTagGroupConfig.TagGroupName.c_str());
    printf("%d\n",objTagGroupConfig.CollectionMethod);
    printf("%s\n",objTagGroupConfig.CollectionType.c_str());
    printf("%s\n",objTagGroupConfig.PLCName.c_str());
    printf("%s\n",objTagGroupConfig.PLCDescription.c_str());
    printf("%d\n",objTagGroupConfig.SlaveID);
    printf("%s\n",objTagGroupConfig.ConnectionString.c_str());
    printf("%s\n",objTagGroupConfig.DriverName.c_str());
    printf("%s\n",objTagGroupConfig.DriverFormat.c_str());

    pthread_t threads[NUM_THREADS];
    while(1)
    {
        int i=0;
        if (objTagGroupConfig.DriverName.compare("Modbus TCP") ==0)
        {
            struct structModbusTCP *modbusTCPConfig = (struct structModbusTCP *)malloc(sizeof(struct structModbusTCP));
            vector<string> v{split(objTagGroupConfig.ConnectionString, ';')};
            vector<string> v1{split(v[0], ':')};
            vector<string> v2{split(v[1], ':')};

            modbusTCPConfig->ip_address = v1[1].c_str();
            modbusTCPConfig->port = atoi(v2[1].c_str());
            modbusTCPConfig->slaveid = objTagGroupConfig.SlaveID;
            int rc = pthread_create(&threads[i], NULL, modbustcp, (void *)modbusTCPConfig);
        }
        if (objTagGroupConfig.DriverName.compare("Modbus RTU") ==0)
        {
            int rc = pthread_create(&threads[i], NULL, modbusrtu, (void *)i);
        }

        sleep(1);
    }
pthread_exit(NULL);

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
    pthread_exit(NULL);
}

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
