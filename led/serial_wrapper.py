import serial
import io

class SerialMockup:
    def __init__(self):
        print('Using SerialMockup')
        self.buf = io.BytesIO()

    def write(self, byte):
        self.buf.write(bytes(byte))
        print('write', bytes(byte))

    def readline(self):
        val = self.buf.getvalue()
        print(val.__repr__())
        print('read', val)
        self.buf = io.BytesIO()

    def close(self):
        pass

class SerialWrapper:
    def __init__(self, serial_file, baud_rate=9600):
        try:
            self.ser = serial.Serial(serial_file, 9600)
        except serial.serialutil.SerialException as e:
            print(e)
            self.ser = SerialMockup()

    def write(self, byte):
        return self.ser.write(byte)

    def readline(self):
        return self.ser.readline()

    def close(self):
        return self.ser.close()
