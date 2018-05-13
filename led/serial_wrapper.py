import serial
import io

class SerialMockup:
    def __init__(self, db=True):
        self.db = db
        if self.db:
            print('Using SerialMockup')
        self.buf = io.BytesIO()

    def inWaiting(self):
        return 1

    def write(self, byte):
        self.buf.write(bytes(byte))
        if self.db:
            print('writing', bytes(byte))

    def readline(self):
        val = self.buf.getvalue()
        if self.db:
            print(val.__repr__())
            print('reading', val)
        self.buf = io.BytesIO()

    def close(self):
        pass

class SerialWrapper:
    def __init__(self, serial_file, db=False, baud_rate=9600):
        self.db = db
        try:
            self.ser = serial.Serial(serial_file, 9600)
            if self.db:
                print('serial opened')
        except serial.serialutil.SerialException as e:
            print(e)
            self.ser = SerialMockup()

    def write(self, byte):
        if self.db:
            print('writing', bytes(byte))
        return self.ser.write(byte)

    def readline(self):
        byte = self.ser.readline()
        if self.db:
            print('reading', byte)
        return byte

    def close(self):
        print('closing')
        return self.ser.close()
