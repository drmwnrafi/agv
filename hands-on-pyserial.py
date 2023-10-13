import serial
import serial.tools.list_ports
import crcmod

# ports = serial.tools.list_ports.comports()

# for port, desc, hwid in sorted(ports):
#         print("{} : {}".format(port, desc))

serial = serial.Serial("COM7", 
                       baudrate = 115200,
                       stopbits=serial.STOPBITS_ONE,
                       parity = serial.PARITY_NONE,
                       bytesize=serial.EIGHTBITS,)

def send_moto
crc8 = crcmod.predefined.mkCrcFun('crc-8-maxim')

input_hex = "02 64 00 00 00 00 00 00 00"

hex_bytes = input_hex.split()
byte_string = bytes(int(byte, 16) for byte in hex_bytes)

checksum = bytes([crc8(byte_string)])
command = byte_string + checksum
print(f"SENDING COMMAND : {command}")

serial.write(command)