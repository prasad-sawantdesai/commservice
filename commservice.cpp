#include <iostream>
#include <cstdlib>
#include <pthread.h>

#include "modbus.h"



using namespace std;

#define NUM_THREADS 5

void *PrintHello(void *threadid) {
   long tid;
   tid = (long)threadid;
   cout << "Hello World! Thread ID, " << tid << endl;
   pthread_exit(NULL);
}

void *modbustcp(void *slaveid)
{
   int sid;
   sid = (long)slaveid;
    // create a modbus object
    modbus mb = modbus("127.0.0.1", 502);


    // set slave id
    cout<<"connected to ";
    cout<<sid;
    mb.modbus_set_slave_id(sid);

    // connect with the server
    mb.modbus_connect();

    // read coil                        function 0x01
    bool read_coil;
    mb.modbus_read_coils(0, 1, &read_coil);
    cout<<read_coil;
	cout<<"\n";
    // read input bits(discrete input)  function 0x02
    bool read_bits;
    mb.modbus_read_input_bits(0, 1, &read_bits);


    // read holding registers           function 0x03
    uint16_t read_holding_regs[1];
    mb.modbus_read_holding_registers(0, 1, read_holding_regs);
    cout<<read_holding_regs[0];


    // read input registers             function 0x04
    uint16_t read_input_regs[1];
    mb.modbus_read_input_registers(0, 1, read_input_regs);


    // write single coil                function 0x05
    mb.modbus_write_coil(0, true);



    // write single reg                 function 0x06
    mb.modbus_write_register(0, 123);


    // write multiple coils             function 0x0F
    bool write_cols[4] = {true, true, true, true};
    mb.modbus_write_coils(0,4,write_cols);


    // write multiple regs              function 0x10
    uint16_t write_regs[4] = {123, 123, 123};
    mb.modbus_write_registers(0, 4, write_regs);


    // close connection and free the memory
    mb.modbus_close();
    //delete(&mb);
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
