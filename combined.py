import pymodbus
from pymodbus.pdu import ModbusRequest
from pymodbus.client import ModbusSerialClient
from pymodbus.transaction import ModbusRtuFramer
import time
import serial
import serial.tools.list_ports
import crcmod

def conversion(value):
    median = (value-256)*0.00390625+1
    if median % 1 != 0:
        median = median + 0.5
    return median

def send_to_motor(command:str):
    crc8 = crcmod.predefined.mkCrcFun('crc-8-maxim')
    hex_bytes = command.split()
    byte_string = bytes(int(byte, 16) for byte in hex_bytes)
    checksum = bytes([crc8(byte_string)])
    command_bytes = byte_string + checksum
    return command_bytes

client = ModbusSerialClient(method='rtu', port='COM7', baudrate=115200, parity='N', timeout=1)
connection = client.connect()

while True:
    read_vals  = client.read_holding_registers(0, 2, slave=5)
    median = conversion(read_vals.registers[0])
    print(median)
    if median == 2.00:
        print(f"Motor 50 RPM")
        command = send_to_motor("02 64 00 32 00 00 00 00 00")
        client.send(command)
    elif median == 15.00:
        print("Motor 0 RPM")
        command = send_to_motor("02 64 00 00 00 00 00 00 00")
        client.send(command)
    time.sleep(0.5)