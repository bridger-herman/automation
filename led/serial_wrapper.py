import serial
import io

from serial_mockup import SerialMockup

class SerialWrapper:
    def __init__(self, serial_file, db=False, baud_rate=9600):
        self.db = db
        self.mockup = False
        try:
            if serial_file is None:
                raise serial.serialutil.SerialException('Board not supplied')
            self.ser = serial.Serial(serial_file, 9600)
            if self.db:
                print('serial opened')
        except serial.serialutil.SerialException as e:
            print(e)
            self.mockup = True
            self.ser = SerialMockup()

    def write(self, byte):
        if self.db:
            print('writing', bytes(byte))
        b = self.ser.write(byte)
        return b

    def inWaiting(self):
        if self.mockup:
            return 1
        else:
            return self.ser.inWaiting()

    def readline(self):
        bytes = self.ser.readline()
        if self.db:
            print('reading', bytes)
        return bytes

    def read(self, num_bytes):
        bytes = self.ser.read(num_bytes)
        return bytes

    def flush(self):
        return self.ser.flush()

    def close(self):
        if self.db:
            print('closing')
        return self.ser.close()
