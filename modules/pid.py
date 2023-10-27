class PID(object):
    def __init__(self, kp, ki, kd, target):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = target
        self.error = 0
        self.last_error = 0
        self.integral_error = 0
        self.derivative_error = 0

    def calculate(self, current_point, max_speed, min_speed, time_step=0.001):
        self.error = self.setpoint - current_point
        self.integral_error += self.error * time_step
        self.derivative_error = (self.error - self.last_error) / time_step
        output = self.kp*self.error + self.ki*self.integral_error + self.kd*self.derivative_error
        if output >= max_speed :
            output = max_speed
        elif output <= min_speed:
            output = min_speed
        return output