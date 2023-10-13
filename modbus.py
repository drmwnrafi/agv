import pymodbus
from pymodbus.pdu import ModbusRequest
from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
import time

client = ModbusClient(method='rtu', port="COM7", baudrate=115200, parity='N', timeout=1)
connection = client.connect()

def conversion(value):
    median = (value-256)*0.00390625+1
    if median % 1 != 0:
        median = median + 0.5
    return median


while True:
    read_vals  = client.read_holding_registers(0, 2, slave=5)
    median = conversion(read_vals.registers[0])
    print(median)
    time.sleep(0.2)