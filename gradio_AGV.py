import gradio as gr
from pymodbus.client import ModbusSerialClient
import utils

client = ModbusSerialClient(method='rtu', port="/dev/ttyUSB1", baudrate=115200, parity='N', timeout=1)
connection = client.connect()
mode = "velocity"

toggle_line = 0

def up():
    utils.send_to_motor(1, -25, mode, client)
    utils.send_to_motor(2, 25, mode, client)
    print("Robot should be moved")
    return "Forward"

def down():
    utils.send_to_motor(1, 25, mode, client)
    utils.send_to_motor(2, -25, mode, client)
    print("Robot should be moved")
    return "Backward"

def left_up():
    utils.send_to_motor(1, -25, mode, client)
    utils.send_to_motor(2, 0, mode, client)
    print("Robot should be moved")
    return "Left"

def right_up():
    utils.send_to_motor(1, 0, mode, client)
    utils.send_to_motor(2, 25, mode, client)
    print("Robot should be moved")
    return "Right"

def left_down():
    utils.send_to_motor(1, 25, mode, client)
    utils.send_to_motor(2, 0, mode, client)
    print("Robot should be moved")
    return "Left"

def right_down():
    utils.send_to_motor(1, 0, mode, client)
    utils.send_to_motor(2, -25, mode, client)
    print("Robot should be moved")
    return "Right"

def right_curve():
    utils.send_to_motor(1, -25, mode, client)
    utils.send_to_motor(2, -25, mode, client)
    print("Robot should be moved")
    return "Right"

def left_curve():
    utils.send_to_motor(1, 25, mode, client)
    utils.send_to_motor(2, 25, mode, client)
    print("Robot should be moved")
    return "Left"

def stop():
    global line_follow 
    line_follow = 0
    utils.send_to_motor(1, 0, mode, client)
    utils.send_to_motor(2, 0, mode, client)
    print("Robot should stop here")
    return "Stop"

def line():
    global line_follow, line_thread
    line_follow = 1
    set_point = 8.51953125
    temp_sensor = None

    while line_follow == 1:
        read = client.read_holding_registers(0, 2, 3)
        sensor = utils.conversion_magnetic(read.registers[0])
        print(sensor)
        if sensor > set_point or temp_sensor == 16:
            utils.send_to_motor(1, -10, mode, client)
            utils.send_to_motor(2, 25, mode, client)
        elif sensor < set_point or temp_sensor == 0:
            utils.send_to_motor(1, -25, mode, client)
            utils.send_to_motor(2, 10, mode, client)
        temp_sensor = sensor

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


if __name__=="__main__":
  try:
    demo.launch()
  except KeyboardInterrupt:
    demo.clear()
    demo.close()
  except Exception as e:
    demo.clear()
    demo.close()