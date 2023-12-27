import wo as wo
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation

robot = wo.Odometry(wheel_radius=0.05, wheelbase=0.432)

rpm_L = []
rpm_R = []

with open("/home/ziczac/dev/agv/rpm_data.txt", "r") as file:
    for line in file:
        rpm_left, rpm_right = map(int, line.strip().split(','))
        
        rpm_L.append(rpm_left)
        rpm_R.append(-rpm_right)
    

x_data = []
y_data = []

def update_plot(frame):
    print(frame)

    angular_vel_L = (rpm_L[frame] * 2 * math.pi / 60.0)
    angular_vel_R = (rpm_R[frame] * 2 * math.pi / 60.0)
    print(angular_vel_L, angular_vel_R)

    robot.non_linear_state_space(angular_vel_L, angular_vel_R, 0.001)

    x, y, _ = robot.get_pose()

    x_data.append(x)
    y_data.append(y)

    plt.clf()
    plt.plot(x_data, y_data, marker='o', linestyle='-', color='b')
    plt.title('Robot Trajectory')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
 
ani = animation.FuncAnimation(plt.gcf(), update_plot, frames=len(rpm_L), interval=1, repeat=False)

plt.show()


