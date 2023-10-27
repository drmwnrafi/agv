import serial

class MAGNET(object):
    def __init__(self, id : int, client : serial.Serial):
        self.id = id
        self.client = client
        self.id_bytes = self.id.to_bytes(1, 'big')

    def median_conversion(self, value:int) -> float:
        median = (value-256)*0.00390625+1
        if median % 1 != 0:
            median = round(median + 0.5, 1)
        return median
    
    def read_sensor(self, line_follow, length, fc = 3):
        last_output = None
        second_output = None
        third_output = None
        fourth_output = None
        fifth_output = None

        fc = fc.to_bytes(1, byteorder='big')
        length = length.to_bytes(1, byteorder='big')

        while line_follow == 1:
            out = client.read(1)

            fifth_output = fourth_output
            fourth_output = third_output
            third_output = second_output
            second_output = last_output
            last_output = out

            if third_output == length and fourth_output == fc and fifth_output == self.id_bytes:
                value = int.from_bytes(second_output+last_output, byteorder='big')
                return value

