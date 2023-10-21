import utils
from pymodbus.client import ModbusSerialClient
import time
import serial

client = ModbusSerialClient(method='rtu', port="/dev/ttyUSB0", baudrate=115200, parity='N', timeout=1)
connection = client.connect()
mode = "velocity"

utils.send_to_motor(1, -25, mode, client)
utils.send_to_motor(2, 25, mode, client)

time.sleep(2)

utils.send_to_motor(1, 0, mode, client)
utils.send_to_motor(2, 0, mode, client)

