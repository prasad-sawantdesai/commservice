#ifndef LIBMODBUSCLIENT_H
#define LIBMODBUSCLIENT_H
#include <string>
#include "modbus.h"
using namespace std;
class LibModbusClient
{
public:
    /** Default constructor */
    LibModbusClient();
    /** Default destructor */
    virtual ~LibModbusClient();

    /** Access m_Counter
     * \return The current value of m_Counter
     */
    //unsigned int GetCounter() { return mb; }
    /** Set m_Counter
     * \param val New value to set
     */
    //void SetCounter(unsigned int val) { m_Counter = val; }
    modbus_t* mb; //!< Member variable

    LibModbusClient CreateTcpClient(string, int);

    LibModbusClient CreateRtuClient(string, int, char, int, int);
    int SetSlaveID(int);
    uint8_t* ReadOutputCoils(int, int);
    uint16_t* ReadHoldingRegisters(int, int);
    uint16_t* ReadInputRegisters(int, int);
    uint8_t* ReadDiscreteInputs(int, int);
    int connect();
    void close();
    int flush();
protected:

private:

};

#endif // LIBMODBUSCLIENT_H
