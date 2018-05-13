import serial
import io

class SerialMockup:
    def __init__(self, db=True):
        self.db = db
        if self.db:
            print('Using SerialMockup')
        self.buf = io.BytesIO()

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
        return self.ser.write(byte)

    def inWaiting(self):
        if self.mockup:
            return 1
        else:
            return self.ser.inWaiting()

    def readline(self):
        byte = self.ser.readline()
        if self.db:
            print('reading', byte)
        return byte

    def close(self):
        print('closing')
        return self.ser.close()
