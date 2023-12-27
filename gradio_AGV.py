import gradio as gr
import utils
import serial
import numpy as np
import time
import matplotlib.pyplot as plt
import time
import ddsm115
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import Localization.wo as wo

plt.style.use('fivethirtyeight')


drive = ddsm115.MotorControl(device="/dev/ttyUSB0")

drive.set_drive_mode(_id=1, _mode=2)
drive.set_drive_mode(_id=2, _mode=2)

kinematics = wo.Odometry(wheel_radius=0.05, wheelbase=0.432)

x_store = []
y_store = []
theta_store = []

mode = "velocity"

line_follow = 0
encoder = 1

def up():
    drive.send_rpm(1, -25)
    drive.send_rpm(2, 25)
    print("Robot should be moved")
    time.sleep(0.25)
    return "Forward"

def down():
    drive.send_rpm(1, 25)
    drive.send_rpm(2, -25)
    print("Robot should be moved")
    time.sleep(0.25)
    return "Backward"

def left_up():
    drive.send_rpm(1, -25)
    drive.send_rpm(2, 0)
    print("Robot should be moved")
    time.sleep(0.25)
    return "Left"

def right_up():
    drive.send_rpm(1, 0)
    drive.send_rpm(2, 25)
    print("Robot should be moved")
    time.sleep(0.25)
    return "Right"

def left_down():
    drive.send_rpm(1, 25)
    drive.send_rpm(2, 0)
    print("Robot should be moved")
    time.sleep(0.25)
    return "Left"

def right_down():
    drive.send_rpm(1, 0)
    drive.send_rpm(2, -25)
    print("Robot should be moved")
    time.sleep(0.25)
    return "Right"

def right_curve():
    drive.send_rpm(1, -25)
    drive.send_rpm(2, -25)
    print("Robot should be moved")
    time.sleep(0.25)
    return "Right"

def left_curve():
    drive.send_rpm(1, 25)
    drive.send_rpm(2, 25)
    print("Robot should be moved")
    time.sleep(0.25)
    return "Left"

def stop():
    global line_follow
    if line_follow == 1:
        line_follow = 0
        time.sleep(0.5)
    drive.send_rpm(1, 0)
    drive.send_rpm(2, 0)
    print("Robot should stop here")
    return "Stop"


def line():
    pass
#     global line_follow
    
#     set_point = 8.5
#     basespeed = 50
#     maxspeed = 65
#     kp, ki, kd = 2, 0, 1

#     temp_sensor = 8.5
#     last_error = 0
#     line_follow = 1
#     i=0
    

#     last_output = None
#     second_output = None
#     third_output = None
#     fourth_output = None
#     fifth_output = None
    
#     v = 8.5

#     time_values = []
#     current_point_values = []
#     set_point_values = []

#     while line_follow == 1:
#         out = client.read(1)

#         fifth_output = fourth_output
#         fourth_output = third_output
#         third_output = second_output
#         second_output = last_output
#         last_output = out

#         if third_output == b'\x04' and fourth_output == b'\x03' and fifth_output == b'\x03':
#             v = int.from_bytes(second_output+last_output, byteorder='big')

#         current_point = utils.conversion_magnetic(v)
#         current_point_values.append(current_point)
#         set_point_values.append(set_point)
#         time_values.append(time.time())

#         print(f"temp : {temp_sensor} || curr : {current_point}")
#         if  current_point == None or current_point > 16 or current_point < 0:
#             current_point = temp_sensor
        
#         current_point_values.append(current_point)
#         set_point_values.append(set_point)
#         time_values.append(time.time())
        
#         error = set_point-current_point
#         p = error
#         i = i + error 
#         d = error - last_error
#         last_error = error
#         motorspeed = p*kp + i*ki + d*kd
#         motor_speed_1 = basespeed + motorspeed
#         motor_speed_2 = basespeed - motorspeed
#         if motor_speed_1 > maxspeed:
#             motor_speed_1 = maxspeed
#         elif motor_speed_2 > maxspeed:
#             motor_speed_2 = maxspeed
#         elif motor_speed_1 < 0:
#             motor_speed_1 = 0
#         elif motor_speed_2 < 0:
#             motor_speed_2 = 0
#         print(motor_speed_2, motor_speed_1)
#         drive.send_rpm(1, -(int(motor_speed_1)))
#         drive.send_rpm(2, int(motor_speed_2))
#         temp_sensor = current_point
#         time.sleep(0.00001)
    
#     with open('data.txt', 'w') as file:
#         file.write("time,current,setpoint\n")
#         for t, cp, sp in zip(time_values, current_point_values, set_point_values):
#             file.write(f"{t},{cp},{sp}\n")

def encoder():
    global encoder, x_store, y_store, theta_store
    global kinematics

    encoder = 1
    
    rpm_left = []
    rpm_right = []

    delta_t = 0.001
    rpm_L = 0
    rpm_R = 0
    while encoder == 1:
        try:
            rpm_L, cur_L = drive.get_motor_feedback(_id=2)
            rpm_R, cur_R = drive.get_motor_feedback(_id=1)
            print(f"RPM : {rpm_L} || RPM : {rpm_R}")

            omega_L = (rpm_L * 2 * np.pi)/60
            omega_R = (-(rpm_R) * 2 * np.pi)/60
            
            kinematics.non_linear_state_space(omega_L, omega_R, delta_t)

            x, y, theta = kinematics.get_pose()

            print(x, y, theta)

            x_store.append(x)
            y_store.append(y)
            theta_store.append(theta)

            time.sleep(delta_t)
        except :
            raise("Error")
    
def end_encoder():
    global encoder, x_store, y_store, theta_store
    encoder = 0
    with open('location.txt', 'w') as file:
        file.write("x, y, theta\n")
        for x, y, theta  in zip(x_store, y_store, theta_store):
            file.write(f"{x}, {y}, {theta}\n")

def inv_kinematics(x_destination = 0.0841, y_destination = -0.00043):
    global kinematics, x, y, theta
    delta_t = 0.001

    while True:
        omega_L, omega_R, l = kinematics.inverse_kinematics([x_destination, y_destination], lyapunov=True)

        rpm_L = (omega_L / (2*np.pi)) * 60
        rpm_R = (omega_R / (2*np.pi)) * 60

        if rpm_L > 100:
            rpm_L = 100
        if rpm_L < -100:
            rpm_L = -100
        if rpm_R > 100:
            rpm_R = 100
        if rpm_R < -100:
            rpm_R = -100

        drive.send_rpm(1, -(rpm_R))
        drive.send_rpm(2, rpm_L)

        rpm_L, cur_L = drive.get_motor_feedback(_id=2)
        rpm_R, cur_R = drive.get_motor_feedback(_id=1)

        omega_L = (rpm_L * 2 * np.pi)/60
        omega_R = (-(rpm_R) * 2 * np.pi)/60

        kinematics.non_linear_state_space(omega_L, omega_R, delta_t)

        x_t, y_t, theta_t = kinematics.get_pose()

        x_store.append(x_t)
        y_store.append(y_t)
        theta_store.append(theta_t)
        # print(x_t, y_t, theta)

        if l < 0.002:
            drive.send_rpm(0, -(rpm_R))
            drive.send_rpm(0, rpm_L)
            time.sleep(0.2)
            break
        
        time.sleep(delta_t)

with gr.Blocks() as demo:
    direction_text = gr.Textbox(label="Robot Direction")

    with gr.Column():
        with gr.Row():
            button_left_up = gr.Button(value="↖️")
            button_up = gr.Button(value="⬆️")
            button_right_up = gr.Button(value="↗️")
        with gr.Row():
            button_left_curve = gr.Button(value="↩️")
            button_stop = gr.Button(value="🛑")
            button_right_curve = gr.Button(value="↪️")
        with gr.Row():
            button_left_down = gr.Button(value="↙️")
            button_down = gr.Button(value="⬇️")
            button_right_down = gr.Button(value="↘️")

    line_follow = gr.Button(value="Line Follower")
    encoders = gr.Button(value="Encoder")
    end_encoders = gr.Button(value="End Encoder")
    inv_kin = gr.Button(value="Inverse Kinematics")


    button_up.click(up, outputs=[direction_text])
    button_down.click(down, outputs=[direction_text])
    button_left_up.click(left_up, outputs=[direction_text])
    button_right_up.click(right_up, outputs=[direction_text])
    button_left_down.click(left_down, outputs=[direction_text])
    button_right_down.click(right_down, outputs=[direction_text])
    button_left_curve.click(left_curve, outputs=[direction_text])
    button_right_curve.click(right_curve, outputs=[direction_text])
    button_stop.click(stop, outputs=[direction_text])
    line_follow.click(line, outputs=[direction_text])
    encoders.click(encoder)
    end_encoders.click(end_encoder)
    inv_kin.click(inv_kinematics)


if __name__=="__main__":
  try:
    demo.launch(share=True)

  except KeyboardInterrupt:
    drive.send_rpm(1, 0)
    drive.send_rpm(2, 0)
    demo.clear()
    demo.close()
  except Exception as e:
    demo.clear()
    demo.close()