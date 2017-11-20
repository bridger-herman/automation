import ctypes
import traceback
import signal
import sys
from serial_wrapper import SerialWrapper

dbprint = print if 'debug' in sys.argv else lambda *args, **kwargs: None

NUM_COLORS = 4

class LEDChanger:
    def __init__(self, serial_wrapper, white=None):
        # Generators for indefinite color
        self.colors = iter([])
        self.delays = iter([])
        self.dones = []
        self.queue = []
        self.white = white
        self.ser = serial_wrapper
        signal.signal(signal.SIGALRM, self._handler)
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
        if self.white != None:
            next_color += white
        color = list(color)
        dbprint('sending', color, delay)
        bytes_send = (ctypes.c_ubyte * len(color))(*color)
        self.ser.write(bytes_send)
        dbprint('sent', color, delay)
        self.dones.append((color, delay))
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
        self.reset()
        signal.setitimer(signal.ITIMER_REAL, 0)

    def reset(self):
        if self.dones:
            colors, delays = zip(*self.dones)
            self.colors, self.delays = iter(colors), iter(delays)

    def __del__(self):
        self.stop()
        self.ser.close()
