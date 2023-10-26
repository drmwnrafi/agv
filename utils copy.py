import crcmod

def extract_sensors_value(serial_client, slave, fn_code=3):
    byte_string = serial_client.read(9)
    if  byte_string != b'' and byte_string[0] == slave and byte_string[1] == fn_code:
        value = int.from_bytes(byte_string[3:-4], byteorder='big')
        return conversion_magnetic(value)

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
    return positive_value

def send_to_motor(id, value, mode, client):
    crc8 = crcmod.predefined.mkCrcFun('crc-8-maxim')
    command = command_conversion(id, value, mode=mode)
    byte_string = bytes(int(byte, 16) for byte in command)
    checksum = bytes([crc8(byte_string)])
    command_bytes = byte_string + checksum
    client.write(command_bytes)

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

def send_command(command:str):
    crc8 = crcmod.predefined.mkCrcFun('crc-8-maxim')
    byte_string = bytes.fromhex(command)
    checksum = crc8(byte_string).to_bytes(1, 'big')
    command_bytes = byte_string + checksum
    return command_bytes


def get_feedback_rpm(id):
    command = f"{id:02d} 74 00 00 00 00 00 00 00"
    command = send_command(command)
    # client.write(command)
    # v_fb = int.from_bytes(client.read(10)[4:6], byteorder='little')
    return command

command = "00 32"
id = 1
print(bytes.fromhex(command))
print(send_command("01 64 FF CE 00 00 00 00 00"))
bytess = twos_complement_to_hex(50, 16).to_bytes(2, byteorder='big')
print(bytess)
