import matplotlib.pyplot as plt
import numpy as np
from wo import Odometry

robot_nonlinear = Odometry(wheel_radius=0.05, wheelbase=0.432)
robot_linear = Odometry(wheel_radius=0.05, wheelbase=0.432)

rpm_L = []
rpm_R = []

with open("/home/ziczac/dev/agv/rpm_data.txt", "r") as file:
    for line in file:
        rpm_left, rpm_right = map(int, line.strip().split(','))
        
        rpm_L.append(rpm_left)
        rpm_R.append(-(rpm_right))

x_data_nonlinear, y_data_nonlinear = [], []
x_data_linear, y_data_linear = [], []

for frame in range(len(rpm_L)):
    rpm_left = rpm_L[frame]
    rpm_right = rpm_R[frame]

    angular_vel_L = (rpm_left * 2 * np.pi) / 60
    angular_vel_R = (rpm_right * 2 * np.pi) / 60

    robot_nonlinear.non_linear_state_space(angular_vel_L, angular_vel_R, 0.001)
    robot_linear.linear_state_space(angular_vel_L, angular_vel_R, 0.001)

    x_nl, y_nl, _ = robot_nonlinear.get_pose()
    x_ll, y_ll, _ = robot_linear.get_pose()

    x_data_nonlinear.append(x_nl)
    y_data_nonlinear.append(y_nl)

    x_data_linear.append(x_ll)
    y_data_linear.append(y_ll)

# Plotting side by side
plt.figure(figsize=(12, 5))

# Plot for nonlinear model
plt.subplot(1, 2, 1)
plt.plot(x_data_nonlinear, y_data_nonlinear, marker='o', linestyle='-', color='b')
plt.title('Nonlinear Model')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')

# Plot for linear model
plt.subplot(1, 2, 2)
plt.plot(x_data_linear, y_data_linear, marker='o', linestyle='-', color='r')
plt.title('Linear Model')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')

plt.tight_layout()
plt.show()
