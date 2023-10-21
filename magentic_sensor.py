import pymodbus
from pymodbus.client import ModbusSerialClient
import utils
import time

client = ModbusSerialClient(method='rtu', port="/dev/ttyUSB0", baudrate=115200, parity='N', timeout=1)
connection = client.connect()
mode = 'velocity'
set_point = 8
temp_sensor = None

while True:
    try :
        read = client.read_holding_registers(0, 2, 5)
        sensor = utils.conversion_magnetic(read.registers[0])
        print(sensor)
        
        if sensor > set_point or temp_sensor == 16:
            utils.send_to_motor(1, -10, mode, client)
            utils.send_to_motor(2, 25, mode, client)
        
        elif sensor < set_point or temp_sensor == 0:
            utils.send_to_motor(1, -25, mode, client)
            utils.send_to_motor(2, 10, mode, client)
        
        temp_sensor = sensor
    except KeyboardInterrupt:
        utils.send_to_motor(1, 0, mode, client)
        utils.send_to_motor(2, 0, mode, client)
        client.close()
        break