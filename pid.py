from simple_pid import PID
from pymodbus.client import ModbusSerialClient
import time
import utils

client = ModbusSerialClient(method='rtu', port="/dev/ttyUSB0", baudrate=115200, parity='N', timeout=1)
connection = client.connect()
mode = 'velocity'

pid_motor1 = PID(Kp=1.0, Ki=0.1, Kd=0.01)
pid_motor2 = PID(Kp=1.0, Ki=0.1, Kd=0.01)

setpoint = 8
output_min = -25  
output_max = 25

sensor_value = None

pid_motor1.setpoint = setpoint
pid_motor2.setpoint = setpoint

# while True:
#     try :
#         read = client.read_holding_registers(0, 2, 5)
#         sensor_value = utils.conversion_magnetic(read.registers[0])

#         motor1_output = pid_motor1(sensor_value)
#         motor2_output = pid_motor2(sensor_value)

#         motor1_output = max(output_min, min(output_max, motor1_output))
#         motor2_output = max(output_min, min(output_max, motor2_output))

#         print(f"Motor 1 Output: {-(motor1_output)}, Motor 2 Output: {motor2_output}")
#         utils.send_to_motor(1, -(int(motor1_output)), mode, client)
#         utils.send_to_motor(2, int(motor2_output), mode, client)

#         time.sleep(0.1)
#     except :
#         client.close()

# client.write_register(2, 2, 5)
read = client.read_holding_registers(0, 2, 3)

while True:
    try :
        sensor_value = utils.conversion_magnetic(read.registers[0])
        print(sensor_value)
    except :
        print("------")