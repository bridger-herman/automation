import serial
import io
import threading

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
        line = self.buf.readline()
        if self.db:
            print(val.__repr__())
            print('reading', val)
        self.buf = io.BytesIO()
        return line

    def read(self, num_bytes):
        bytes = self.buf.read(num_bytes)
        if self.db:
            print('reading', bytes)
        return bytes

    def close(self):
        pass

class SerialWrapper:
    def __init__(self, serial_file, db=False, baud_rate=9600):
        self.db = db
        self.mockup = False
        # # self.lock = threading.Lock()
        try:
            if serial_file is None:
                raise serial.serialutil.SerialException('Board not supplied')
            self.ser = serial.Serial(serial_file, 9600)
            if self.db:
                print('serial opened')
        except serial.serialutil.SerialException as e:
            print(e)
            self.mockup = True
            # self.ser = SerialMockup()
            self.ser = io.BytesIO()

    def write(self, byte):
        if self.db:
            print('writing', bytes(byte))
        # self.lock.acquire()
        b = self.ser.write(byte)
        # self.lock.release()
        return b

    def inWaiting(self):
        if self.mockup:
            return 1
        else:
            return self.ser.inWaiting()

    def readline(self):
        # self.lock.acquire()
        bytes = self.ser.readline()
        # self.lock.release()
        if self.db:
            print('reading', bytes)
        return bytes

    def read(self, num_bytes):
        # self.lock.acquire()
        bytes = self.ser.read(num_bytes)
        # self.lock.release()
        return bytes

    def flush(self):
        return self.ser.flush()

    def close(self):
        if self.db:
            print('closing')
        return self.ser.close()
