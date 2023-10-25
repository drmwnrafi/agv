from simple_pid import PID
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

basespeed = 18
maxspeed = 25

def pid(kp, ki, kd, current_point, last_error, set_point=8):
    error = set_point-current_point
    p = error
    i = i + error 
    d = error - last_error
    last_error = error
    motorspeed = p*kp + i*ki + d*kd
    motor_speed_1 = basespeed + motorspeed
    motor_speed_2 = basespeed - motorspeed
    if motor_speed_1 > maxspeed:
        motor_speed_1 = maxspeed
    elif motor_speed_2 > maxspeed:
        motor_speed_2 = maxspeed
    elif motor_speed_1 < 0:
        motor_speed_1 = 0
    elif motor_speed_2 < 0:
        motor_speed_2 = 0
    return motor_speed_1, motor_speed_2, last_error

kp, ki, kd = 0.93, 0, 0

i = 0
last_error = 0
last_point = 0

while True:
    current_point = utils.extract_sensors_value(client, 3)
    if  current_point == None:
        current_point = last_point
    last_point = current_point
    error = 8-current_point
    p = error
    i = i + error 
    d = error - last_error
    last_error = error
    motorspeed = p*kp + i*ki + d*kd
    motor_speed_1 = basespeed + motorspeed
    motor_speed_2 = basespeed - motorspeed
    if motor_speed_1 > maxspeed:
        motor_speed_1 = maxspeed
    elif motor_speed_2 > maxspeed:
        motor_speed_2 = maxspeed
    elif motor_speed_1 < 0:
        motor_speed_1 = 0
    elif motor_speed_2 < 0:
        motor_speed_2 = 0
    print(motor_speed_1, motor_speed_2)