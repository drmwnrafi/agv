import serial
import time
import utils

client = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

mode = 'velocity'
temp = None
print(f"Motor 50 RPM")
utils.send_to_motor(1, -25, mode, client)
utils.send_to_motor(2, 25, mode, client)
time.sleep(3)
utils.send_to_motor(1, -0, mode, client)
utils.send_to_motor(2, 0, mode, client)

