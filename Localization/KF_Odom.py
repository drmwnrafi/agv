import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


ang_vel_L = []
ang_vel_R = []

with open("/home/ziczac/dev/agv/rpm_data.txt", "r") as file:
    for line in file:
        rpm_left, rpm_right = map(int, line.strip().split(','))
        
        ang_vel_L.append((rpm_left * 2 * np.pi)/60)
        ang_vel_R.append(-((rpm_right * 2 * np.pi)/60))

# Combine left and right wheel angular velocities
angular_velocity_data = np.column_stack((ang_vel_L, ang_vel_R))

# Kalman filter parameters
dt = 1.0  # Time step
initial_state = np.array([0, 0, 0])  # Initial state [x, y, theta]
initial_covariance = np.diag([1, 1, 1])  # Initial covariance matrix
process_variance = np.diag([0.1, 0.1, 0.1])  # Process noise variance
measurement_variance = np.diag([1, 1])  # Measurement noise variance

import numpy as np

# Define matrices and initial values
A = np.eye(6)  # State transition matrix
B = np.eye(6)  # Control input matrix
H = np.eye(6)  # Observation matrix
Q = np.eye(6)  # Process noise covariance
R = np.eye(6)  # Measurement noise covariance

# Initial state estimate and covariance
global x_hat
x_hat = np.zeros((6, 1))
global P
P = np.eye(6)
# Simulate data (replace with your own data)
left_angular_velocity = np.array(ang_vel_L)
right_angular_velocity = np.array(ang_vel_R)

x_history = []
y_history = []
theta_history = []

# # Kalman filter loop
# for i in range(len(left_angular_velocity)):
#     # Predict
#     u = np.array([left_angular_velocity[i], right_angular_velocity[i], 0, 0, 0, 0]).reshape(-1, 1)
#     x_hat_minus = A.dot(x_hat) + B.dot(u)
#     P_minus = A.dot(P).dot(A.T) + Q

#     # Update
#     z = x_hat_minus  # In this simple example, the measurement is the predicted state itself
#     K = P_minus.dot(H.T).dot(np.linalg.inv(H.dot(P_minus).dot(H.T) + R))
#     x_hat = x_hat_minus + K.dot(z - H.dot(x_hat_minus))
#     P = (np.eye(6) - K.dot(H)).dot(P_minus)

#     x = x_hat[0, 0]
#     y = x_hat[1, 0]
#     theta = x_hat[2, 0]

#     # Store results for plotting
#     x_history.append(x)
#     y_history.append(y)
#     theta_history.append(theta)


def update_plot(frame):
    global x_hat, P
    print(frame)
    u = np.array([left_angular_velocity[frame], right_angular_velocity[frame], 0, 0, 0, 0]).reshape(-1, 1)
    x_hat_minus = A.dot(x_hat) + B.dot(u)
    P_minus = A.dot(P).dot(A.T) + Q

    # Update
    z = x_hat_minus  # In this simple example, the measurement is the predicted state itself
    K = P_minus.dot(H.T).dot(np.linalg.inv(H.dot(P_minus).dot(H.T) + R))
    x_hat = x_hat_minus + K.dot(z - H.dot(x_hat_minus))
    P = (np.eye(6) - K.dot(H)).dot(P_minus)

    x = x_hat[0, 0]
    y = x_hat[1, 0]
    theta = x_hat[2, 0]

    # Store results for plotting
    x_history.append(x)
    y_history.append(y)
    theta_history.append(theta)

    plt.clf()
    plt.plot(x_history, y_history, marker='o', linestyle='-', color='b')
    plt.title('Robot Trajectory')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
 
ani = animation.FuncAnimation(plt.gcf(), update_plot, frames=len(left_angular_velocity), interval=1, repeat=False)

plt.show()

