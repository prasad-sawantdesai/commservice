#include <iostream>
#include "LibModbusClient.h"
#include <cstdlib>
#include <pthread.h>
#include <time.h>
#include "ConfigReader.h"
#include "DatabaseWriter.h"

using namespace std;

#define NUM_THREADS 1

void *modbustcp(void *slaveid)
{
    int sid = (long)slaveid;
    cout<<"Modbus client is connecting to :"<<sid<<endl;

    LibModbusClient obj;

    obj= obj.CreateTcpClient("192.168.1.100",502);
    obj.SetSlaveID(sid);
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
    uint16_t* holding_reg = obj.ReadHoldingRegisters(0, 20);

    for (int i=0; i < 5; i++)
    {
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

int main ()
{
//Read sqlite database

    ConfigReader objConfigReader = ConfigReader();
    objConfigReader.Connect("/home/ujjaini/prasad/commservice/git_repo/commservice/database/commservice.db");

    //connect to mongo db
    DatabaseWriter objDatabaseWriter = DatabaseWriter();
    objDatabaseWriter.Connect("mongodb://localhost:27017");
    pthread_t threads[NUM_THREADS];
    int rc;
    int i;

    for( i = 0; i < NUM_THREADS; i++ )
    {
        cout << "\nmain() : creating tcp modbus connection thread, " << i << endl;
        rc = pthread_create(&threads[i], NULL, modbustcp, (void *)i);

        //cout << "\nmain() : creating rtu modbus connection thread, " << i << endl;
        //rc = pthread_create(&threads[i], NULL, modbusrtu, (void *)i);

        if (rc)
        {
            cout << "\n Error:unable to create thread," << rc << endl;
            exit(-1);
        }
    }
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
