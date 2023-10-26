import matplotlib.pyplot as plt
import random
import time

time_stamp = 0.001
sensors = []

time_end = time.time() + 1

while time.time() <= time_end:
    rnd = random.randint(1,16)
    sensors.append(rnd)
    time.sleep(time_stamp)

plt.plot(sensors)
plt.xlabel('Time (s)')
plt.ylabel('Sensor Reading')
plt.title('Sensor Readings Over Time')
plt.show()