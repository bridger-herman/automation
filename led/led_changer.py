import serial
import ctypes
import logging
import io
import time
import traceback

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
        sleep_time = int(val[-2])*int(val[-1])
        time.sleep(sleep_time / 1000.0) # TODO no magic numbers
        self.buf = io.BytesIO()

    def close(self):
        pass

class SerialLEDChanger:
    def __init__(self, alpha=None):
        # Generators for indefinite color
        self.colors = None
        self.delays = None
        self.alpha = alpha
        try:
            #  self.ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
            self.ser = serial.Serial('/dev/ttyACM0', 9600)
            self.ser.readline() # Priming read, for some reason?
        except serial.serialutil.SerialException:
            print('tb',traceback.format_tb())
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
                delay, multiple = self.__seperate_duration(next_delay)
                color_delay_multiple = list(next_color) + [delay] + [multiple]
                bytes_send = (ctypes.c_ubyte * len(color_delay_multiple)) \
                        (*color_delay_multiple)
                self.ser.write(bytes_send)
                self.ser.readline() # Did the Arduino receive?

    def stop(self):
        self.active = False

    def __del__(self):
        self.ser.close()

    def __seperate_duration(self, duration):
        new_duration = duration
        multiplier = 0
        # TODO get actual max eventually, do while...
        while multiplier <= 0 or new_duration > 255:
            multiplier += 1
            new_duration = duration // multiplier
        return new_duration, multiplier

if __name__ == '__main__':
    s = SerialLEDChanger()
    s.colors = ((5, 5, 5, 5) for i in range(5))
    s.delays = (500 for i in range(5))
    s.start()
