#include "LibModbusClient.h"
#include <string>
#include <iostream>

using namespace std;

LibModbusClient::LibModbusClient()
{
    //constructor code
}

LibModbusClient::~LibModbusClient()
{
    //destructor code
}

LibModbusClient LibModbusClient::CreateTcpClient(string ip_address, int port)
{
    LibModbusClient object = LibModbusClient();

    object.mb = modbus_new_tcp(ip_address.c_str(), port);
    return object;
}

LibModbusClient LibModbusClient::CreateRtuClient(string port,int baudrate,char parity,int bytesize,int stopbits)
{
    LibModbusClient object = LibModbusClient();

    object.mb = modbus_new_rtu(port.c_str(), baudrate, parity, bytesize, stopbits);
    if (object.mb == NULL) {
        fprintf(stderr, "Unable to create the libmodbus context\n");
    }
    return object;
}

int LibModbusClient::connect()
{
    int ret = modbus_connect(mb);
    if ( ret== -1)
    {
        fprintf(stderr, "Connection failed: %s\n", modbus_strerror(errno));
        modbus_free(mb);
    }
    return ret;
}
int LibModbusClient::SetSlaveID(int slaveid)
{
    int rc;
    rc = modbus_set_slave(mb, slaveid);
    if (rc == -1)
    {
        fprintf(stderr, "Invalid slave ID\n");
        modbus_free(mb);
        return -1;
    }
    return 0;
}

uint16_t* LibModbusClient::ReadHoldingRegisters(int address, int number)
{
    /** Read holding registers
    parameters:
    address : address of variable
    number : number of values

    * \return array of values
    */

    uint16_t* tab_reg =  new uint16_t[number];

    int rc = modbus_read_registers(mb, address, number, tab_reg);
    if (rc == -1)
    {
        fprintf(stderr, "%s\n", modbus_strerror(errno));
        return NULL;
    }
    return tab_reg;
}

uint16_t* LibModbusClient::ReadInputRegisters(int address, int number)
{
    /** Read input registers
    parameters:
    address : address of variable
    number : number of values

    * \return array of values
    */
    uint16_t* tab_reg =  new uint16_t[number];

    int rc = modbus_read_input_registers(mb, address, number, tab_reg);
    if (rc == -1)
    {
        fprintf(stderr, "%s\n", modbus_strerror(errno));
        return NULL;
    }
    return tab_reg;
}

uint8_t* LibModbusClient::ReadInputCoils(int address, int number)
{
    /** Read input coils
    parameters:
    address : address of variable
    number : number of values

    * \return array of values
    */
    uint8_t* tab_reg =  new uint8_t[number];

    int rc = modbus_read_bits(mb, address, number, tab_reg);
    if (rc == -1)
    {
        fprintf(stderr, "%s\n", modbus_strerror(errno));
        return NULL;
    }
    return tab_reg;
}

int LibModbusClient::flush()
{
    return modbus_flush(mb);
}

void LibModbusClient::close()
{
    modbus_close(mb);
    modbus_free(mb);
}



//        rc = modbus_write_register(mb, 0, 45);
//    rc = modbus_write_register(mb, 1, 65);
//    rc = modbus_write_register(mb, 2, 85);
//    rc = modbus_write_register(mb, 2, 120);
/*
int modbus_read_input_bits(modbus_t *ctx, int addr, int nb, uint8_t *dest);
int modbus_read_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest);
int modbus_read_input_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest);
int modbus_report_slave_id(modbus_t *ctx, int max_dest, uint8_t *dest);*/
