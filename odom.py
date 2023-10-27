from math import cos, sin,radians, degrees
import matplotlib.pyplot as plt
import utils
import serial
import time

client = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)

x_local = 0
y_local = 0
psi = 0
vx_local = 0
vy_local = 0

def hitung(kanan, kiri):
    global x_local, y_local, psi, vx_local, vy_local

    radius = 0.05
    wheelbase = 0.433

    # deg/s
    v_motor_kanan = kanan/60*radius
    v_motor_kiri = kiri/60*radius

    omega = radius*(v_motor_kanan-v_motor_kiri)/wheelbase
    psi += omega

    if psi > 360:
        psi -= 360
    elif psi < 0:
        psi+=360

    vx_local = radius*(v_motor_kanan*cos(radians(psi))+v_motor_kiri*cos(radians(psi)))/2
    vy_local = radius*(v_motor_kanan*sin(radians(psi))+v_motor_kiri*sin(radians(psi)))/2

    x_local += vx_local
    y_local += vy_local

    return x_local, y_local

x_history = []
y_history = []

value1 = 25

start_time = time.time()

# utils.send_to_motor(1, 0, 'velocity', client)
# utils.send_to_motor(2, 0, 'velocity', client)

while time.time() - start_time <= 10:  # Run for 10 seconds
    current_time = time.time() - start_time  # Calculate elapsed time

    if current_time < 5:
        x, y = hitung(25, 25)
        x_history.append(x)
        y_history.append(y)
        time.sleep(0.001)
    elif current_time < 3:
        x, y = hitung(0, 330)
        x_history.append(x)
        y_history.append(y)
        time.sleep(0.001)
    elif current_time < 3:
        x, y = hitung(330,0)
        x_history.append(x)
        y_history.append(y)
        time.sleep(0.001)
    else:
        x, y = hitung(25, 25)
        x_history.append(x)
        y_history.append(y)
        time.sleep(0.001)


plt.figure()
plt.plot(x_history, y_history, label='Robot Path')
plt.xlabel('X Local (m)')
plt.ylabel('Y Local (m)')
plt.title('Robot Movement')
plt.legend()
plt.grid()
plt.axis('equal')
plt.show()