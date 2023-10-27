import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())

if len(ports) == 0:
    print("No serial ports found.")
else:
    print("Available serial ports:")
    for port, desc, hwid in ports:
        print(f"Port: {port}, Description: {desc}")