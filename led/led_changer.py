import serial
import ctypes
import io
import traceback
import signal
import sys

dbprint = print if 'debug' in sys.argv else lambda *args, **kwargs: None

class SerialMockup:
    def __init__(self):
        dbprint('Using SerialMockup')
        self.buf = io.BytesIO()

    def write(self, byte):
        self.buf.write(bytes(byte))
        dbprint('write', bytes(byte))

    def readline(self):
        val = self.buf.getvalue()
        dbprint(val.__repr__())
        dbprint('read', val)
        self.buf = io.BytesIO()

    def close(self):
        pass

class SerialLEDChanger:
    def __init__(self, alpha=None):
        # Generators for indefinite color
        self.colors = None
        self.delays = None
        self.queue = []
        self.alpha = alpha
        signal.signal(signal.SIGALRM, self._handler)
        try:
            #  self.ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
            self.ser = serial.Serial('/dev/ttyACM0', 9600)
        except serial.serialutil.SerialException:
            dbprint('tb',traceback.format_tb())
            self.ser = SerialMockup()
        self.active = False

    def _handler(self, signum, frame):
        dbprint('handled!')
        try:
            incoming = self.ser.readline()
            dbprint('readline', incoming)
            next_color = next(self.colors)
            next_delay = next(self.delays)
            self.queue.insert(0, (next_color, next_delay))
            dbprint('queuing', next_color, next_delay)
        except StopIteration:
            self.stop()
        else:
            self._send()

    def _send(self):
        color, delay = self.queue.pop()
        if self.alpha != None:
            next_color += alpha
        color = list(color)
        dbprint('sending', color, delay)
        bytes_send = (ctypes.c_ubyte * len(color))(*color)
        self.ser.write(bytes_send)
        dbprint('sent', color, delay)
        signal.setitimer(signal.ITIMER_REAL, delay)

    def start(self):
        self.active = True
        self._handler(0, 0)
        # Spin until we're done here
        while self.active:
            pass

    def stop(self):
        dbprint('stopped')
        self.active = False
        while len(self.queue) > 0:
            self._send()
        signal.setitimer(signal.ITIMER_REAL, 0)

    def __del__(self):
        self.stop()
        self.ser.close()

if __name__ == '__main__':
    s = SerialLEDChanger()
    s.colors = ((i, i, i, i) for i in range(0, 255, 49))
    s.delays = (0.5 for i in range(6))
    s.start()
