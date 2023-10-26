import utils
from pymodbus.client import ModbusSerialClient
import serial
import time

client = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

utils.send_to_motor(1, 0, 'velocity', client)

while True:
    com = utils.send_command("01 74 00 00 00 00 00 00 00")
    client.write(com)
    time.sleep(0.1)
    v_fb = client.read(10)
    print(int.from_bytes(v_fb[4:6], byteorder='little'))
