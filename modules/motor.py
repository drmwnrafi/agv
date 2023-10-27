import serial
import crcmod

map = lambda x, in_min, in_max, out_min, out_max: (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
constrain = lambda x, min, max: min if x < min else max if x > max else x

class MOTOR(object):
    def __init__(self, client : serial.Serial, id  : int) -> None:
        self.client = client
        self.id = id
        self.crc8 = crcmod.predefined.mkCrcFun('crc-8-maxim')

    def generate_command_str(self, command:str) -> bytes:
        command = bytes.fromhex(command)
        checksum = self.crc8(command).to_bytes(1, 'big')
        return command + checksum
    
    def twos_complement(self, value:int, num_bits:int) -> bytes:
        """
        return value in dtype bytes
        """

        if value < 0:
            positive_value = value.to_bytes(int(num_bits/8), 'big', signed=True)
        else:
            positive_value = value.to_bytes(int(num_bits/8), 'big')
        return positive_value
    
    def send_to_motor(self, mode:str, value:int) -> None:
        """
        send command directly to motor
        """

        if mode.lower() == "current" :
            value = map(constrain(value, -8, 8), -8, 8, -32767, 32767)
        elif mode.lower() == "position" :
            value = map(constrain(value, 0, 360), 0, 360, 0, 32767)
        elif mode.lower() == "velocity" :
            value = value 

        value = self.twos_complement(value, num_bits=16)
        command = self.id.to_bytes(1, 'big') + b'd%b\x00\x00\x00\x00\x00'%value
        checksum = self.crc8(command).to_bytes(1, 'big')
        command_bytes = command + checksum
        self.serial.write(command_bytes)
    
    def get_feedback(self) -> int:
        command = f"{self.id:02d} 74 00 00 00 00 00 00 00"
        command = self.generate_command_str(command)
        self.client.write(command)
        output = self.client.read(10)

        v_fb = int.from_bytes(output[4:6], byteorder='little')
        torque_fb = int.from_bytes(output[2:3], byteorder='little')
        mode = int.from_bytes(output[1], byteorder='big')

        vel = map(constrain(v_fb,-32767,32767), -32767, 32767, -330, 330)
        return mode, torque_fb, vel
    
    def get_linear_velocity(self, radius) -> float:
        """
        radius : Any = radius of wheel
        """
        mode, tor, vel = self.get_feedback()
        if vel is None:
            return None
        return vel/60 * radius