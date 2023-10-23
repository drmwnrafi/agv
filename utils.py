import crcmod
import binascii

def extract_sensors_value(serial_client, slave):
    byte_string = serial_client.read(9)
    if byte_string[0] == slave:
        hex_string = binascii.hexlify(byte_string).decode('utf-8')
        hex_list = [hex(i) for i in byte_string]
        value = hex_list[3:-4]
        combined_hex = (int(value[0], 16) << 8) | int(value[1], 16)
    return conversion_magnetic(combined_hex)

def conversion_magnetic(value):
    median = (value-256)*0.00390625+1
    if median % 1 != 0:
        median = median + 0.5
    return median

def map_value(inp_val, inp_min, inp_max, out_min, out_max):
    out_val = int((inp_val-inp_min)/(inp_max-inp_min) * (out_max-out_min) + out_min)
    return out_val

def twos_complement_to_hex(twos_complement, num_bits):
    if twos_complement < 0:
        positive_value = (abs(twos_complement) ^ (1 << num_bits)-1) + 1
        # positive_value = (twos_complement & (1 << num_bits)-1)
    else:
        positive_value = twos_complement
    hex_value = f"{positive_value:0{num_bits//4}x}"
    return hex_value

def command_conversion(id:int, value:int, mode:str, bits=16):
    if mode.lower() == "current" :
        value = map_value(value, -8, 8, -32767, 32767)
    elif mode.lower() == "position" :
        value = map_value(value, 0, 360, 0, 32767)
    elif mode.lower() == "velocity" :
        value = value
    value = twos_complement_to_hex(value, num_bits=bits).upper()
    command = [f"{id:02d}", "64", value[:2], value[2:], "00", "00", "00", "00", "00"]
    return command

def send_to_motor(id, value, mode, client):
    crc8 = crcmod.predefined.mkCrcFun('crc-8-maxim')
    command = command_conversion(id, value, mode=mode)
    byte_string = bytes(int(byte, 16) for byte in command)
    checksum = bytes([crc8(byte_string)])
    command_bytes = byte_string + checksum
    # print(command_bytes, checksum)
    client.send(command_bytes)

def send_command(command:str):
    crc8 = crcmod.predefined.mkCrcFun('crc-8-maxim')
    command=command.split()
    byte_string = bytes(int(byte, 16) for byte in command)
    checksum = bytes([crc8(byte_string)])
    command_bytes = byte_string + checksum
    return command_bytes
