import math
import numpy as np

class Odometry:
    def __init__(self, wheelbase, wheel_radius):
        """
        wheelbase : meters
        wheel_raddius : meters
        """
        self.wheelbase = wheelbase
        self.wheel_radius = wheel_radius
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.v = 0.0
        self.omega = 0.0
        self.gaussian_noise = np.random.normal(0, 0.001, 3)
    
    def normalize_angle(self, angle):
        return (angle + 2.0 * math.pi) % (2.0 * math.pi)

    def non_linear_state_space(self, left_angular, right_angular, delta_t):
        """
        left_angular : rad/s
        right_angular : rad/s
        """

        vl = self.wheel_radius * left_angular 
        vr = self.wheel_radius * right_angular
        v = (vr + vl) / 2.0

        omega = (vr - vl)/self.wheelbase 

        self.x += v * math.cos(self.theta) * delta_t
        self.y += v * math.sin(self.theta) * delta_t
        self.theta += omega * delta_t

    def inverse_kinematics(self, target_pose:list, lyapunov = True, k_psi = 2, k_l=3):
        """
        target_pose : (x, y) coordinates
        k_psi : constant gain for psi (theta destination - theta now)
        k_l : constant gain for l (distance (x, y))
        lyapunov : method for determine angular velocity (omega) robot and linear velocity (v)
        """
        x, y, theta = self.x, self.y, self.theta
        
        dx = target_pose[0] - x
        dy = target_pose[1] - y

        theta_d = np.arctan2(dy, dx)
        l = np.sqrt(dx**2 + dy**2)
        psi = theta_d - theta
        
        if lyapunov :
            v = k_l * l * np.cos(psi)
            omega = k_l * (np.sin(psi) * np.cos(psi)) + k_psi * psi
        else :
            v = k_l * l
            omega = k_psi * psi

        omega_l = ((2 * v) - (omega * self.wheelbase)) / (2 * self.wheel_radius)
        omega_r = ((2 * v) + (omega * self.wheelbase)) / (2 * self.wheel_radius)

        return omega_l, omega_r, l
    
    def linear_state_space(self, left_angular, right_angular, delta_t):
        np.random.seed(42)
        gaussian_noise = np.random.normal(0, 0.001, 3)
        print(gaussian_noise)

        v = (self.wheel_radius / 2.0) * (left_angular + right_angular)
        omega = (self.wheel_radius / self.wheelbase) * (right_angular - left_angular)

        A = np.eye(3)

        B = np.array([[np.cos(self.theta)*delta_t, 0],
                      [np.sin(self.theta)*delta_t, 0],
                      [0, delta_t]])

        U = np.array([self.v, self.omega])
        X_dot = np.array([self.x, self.y, self.theta])

        X = A @ X_dot + B @ U + self.gaussian_noise

        self.x += X[0] * delta_t
        self.y += X[1] * delta_t
        self.theta += X[2] * delta_t
        self.v = v
        self.omega = omega
        self.gaussian_noise = gaussian_noise
        
    def get_pose(self):
        return self.x, self.y, self.theta


        # self.theta = self.normalize_angle(self.theta)

