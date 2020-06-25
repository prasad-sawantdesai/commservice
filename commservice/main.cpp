#include <iostream>
#include "LibModbusClient.h"
#include <cstdlib>
#include <pthread.h>
using namespace std;
#define NUM_THREADS 20
void *modbustcp(void *slaveid)
{
   int sid;
   sid = (long)slaveid;
       cout<<"connected to ";
    cout<<sid;


    LibModbusClient obj;

    obj= obj.CreateTcpClient("127.0.0.1",502);
    obj.SetSlaveID(sid);
    obj.connect();
    uint16_t* array = obj.ReadHoldingRegisters(0, 5);
    obj.close();

    return 0;
}

int main () {
   pthread_t threads[NUM_THREADS];
   int rc;
   int i;

   for( i = 0; i < NUM_THREADS; i++ ) {
      cout << "main() : creating thread, " << i << endl;
      rc = pthread_create(&threads[i], NULL, modbustcp, (void *)i);

      if (rc) {
         cout << "Error:unable to create thread," << rc << endl;
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
