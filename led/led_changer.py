import serial
import ctypes
import logging
import io

class SerialMockup():
    def __init__(self):
        self.buf = io.StringIO()

    def write(self, byte):
        self.buf.write(str(bytes(byte)))
        print('write', bytes(byte))

    def readline(self):
        print('read', self.buf.getvalue())
        self.buf = io.StringIO()

    def close(self):
        pass

class SerialLEDChanger:
    def __init__(self, alpha=None):
        # Generators for indefinite color
        self.colors = None
        self.delays = None
        self.alpha = alpha
        try:
            self.ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
            self.ser.readline() # Priming read, for some reason?
        except serial.serialutil.SerialException:
            self.ser = SerialMockup()
        self.active = False

    def start(self):
        self.active = True
        while self.active:
            try:
                next_color = next(self.colors)
                next_delay = next(self.delays)
            except StopIteration:
                self.active = False
            else:
                if self.alpha != None:
                    next_color += alpha
                color_delay = list(next_color) + [next_delay]
                bytes_send = (ctypes.c_ubyte * len(color_delay)) \
                        (*color_delay)
                self.ser.write(bytes_send)
                self.ser.readline() # Did the Arduino receive?

    def stop(self):
        self.active = False

    def __del__(self):
        self.ser.close()

if __name__ == '__main__':
    s = SerialLEDChanger()
    s.colors = ((5, 5, 5, 5) for i in range(5))
    s.delays = (5 for i in range(5))
    s.start()
