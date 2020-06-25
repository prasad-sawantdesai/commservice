#include "LibModbusClient.h"
#include <string>
#include <iostream>
#include <time.h>
using namespace std;

LibModbusClient::LibModbusClient()
{
    //ctor
}

LibModbusClient::~LibModbusClient()
{

}

LibModbusClient LibModbusClient::CreateTcpClient(string ip_address, int port)
{
    LibModbusClient object = LibModbusClient();
    object.mb = modbus_new_tcp(ip_address.c_str(), port);
    return object;
}

LibModbusClient LibModbusClient::CreateRtuClient(string port,int baudrate,int parity,int bytesize,int stopbits)
{
    LibModbusClient object = LibModbusClient();
    object.mb = modbus_new_rtu(port.c_str(), baudrate, parity, bytesize, stopbits);
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
}

uint16_t* LibModbusClient::ReadHoldingRegisters(int address, int number)
{
    /** Access m_Counter
        rc = modbus_write_register(mb, 0, 45);
    rc = modbus_write_register(mb, 1, 65);
    rc = modbus_write_register(mb, 2, 85);
    rc = modbus_write_register(mb, 2, 120);
    * \return The current value of m_Counter
    */
    time_t my_time = time(NULL);
    uint16_t tab_reg[number];
    int rc;

    rc = modbus_read_registers(mb, address, number, tab_reg);
    if (rc == -1)
    {
        fprintf(stderr, "%s\n", modbus_strerror(errno));
        return NULL;
    }
    for (int i=0; i < rc; i++)
    {
        printf("%s : reg[%d]=%d (0x%X)\n", ctime(&my_time), i, tab_reg[i], tab_reg[i]);
    }
    return tab_reg;
}

uint16_t* LibModbusClient::ReadInputRegisters(int address, int number)
{
    uint16_t tab_reg[number];
    int rc;
    rc = modbus_read_input_registers(mb, address, number, tab_reg);
    if (rc == -1)
    {
        fprintf(stderr, "%s\n", modbus_strerror(errno));
        return NULL;
    }
    return tab_reg;
}

uint8_t* LibModbusClient::ReadInputCoils(int address, int number)
{
    uint8_t tab_reg[number];
    int rc;
    rc = modbus_read_input_bits(mb, address, number, tab_reg);
    if (rc == -1)
    {
        fprintf(stderr, "%s\n", modbus_strerror(errno));
        return NULL;
    }
    return tab_reg;
}
/*
int modbus_read_input_bits(modbus_t *ctx, int addr, int nb, uint8_t *dest);
int modbus_read_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest);
int modbus_read_input_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest);
int modbus_report_slave_id(modbus_t *ctx, int max_dest, uint8_t *dest);*/
int LibModbusClient::flush()
{
    return modbus_flush(mb);
}

void LibModbusClient::close()
{
    modbus_close(mb);
    modbus_free(mb);
}
