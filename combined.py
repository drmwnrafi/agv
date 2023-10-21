from pymodbus.client import ModbusSerialClient
import utils

client = ModbusSerialClient(method='rtu', port='COM7', baudrate=115200, parity='N', timeout=1)
connection = client.connect()

while True:
    read_vals  = client.read_holding_registers(0, 2, slave=5)
    median = utils.conversion(read_vals.registers[0])
    print(median)
    if median == 2.00:
        print(f"Motor 50 RPM")
        command = utils.send_to_motor("02 64 00 32 00 00 00 00 00")
        client.send(command)
    elif median == 15.00:
        print("Motor 0 RPM")
        command = utils.send_to_motor("02 64 00 00 00 00 00 00 00")
        client.send(command)
    time.sleep(0.5)