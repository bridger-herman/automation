import ctypes
import traceback
import signal
import sys
from serial_wrapper import SerialWrapper

dbprint = print if 'debug' in sys.argv else lambda *args, **kwargs: None
MAX_COLORS = 4

import time
TIME = 0

class LEDChanger:
    def __init__(self, serial_wrapper, white=None):
        self.queue = []
        self.dones = []
        self.white = white
        self.ser = serial_wrapper
        signal.signal(signal.SIGALRM, self._handler)
        self.active = False

    def setup(self):
        # Generators for indefinite color
        self.colors = iter([])
        self.delays = iter([])

    def _handler(self, signum, frame):
        dbprint('handled!')
        try:
            if self.ser.ser.inWaiting() > 0:
                incoming = self.ser.readline()
                dbprint('readline', incoming)
            next_color = next(self.colors)
            next_delay = next(self.delays)
            t0 = time.time()
            self.queue.insert(0, (next_color, next_delay))
            t1 = time.time()
            # print('queue', t1 - t0)
            dbprint('queuing', next_color, next_delay)
        except StopIteration:
            self.stop()
        else:
            self._send()

    def _send(self):
        global TIME
        t = time.time()
        print(t - TIME)
        TIME = t
        color, delay = self.queue.pop()
        if self.white != None:
            color += [self.white]
        color = list(color)
        dbprint('sending', color, delay)
        bytes_send = (ctypes.c_ubyte * len(color))(*color)
        t0 = time.time()
        self.ser.write(bytes_send)
        t1 = time.time()
        dbprint('sent', color, delay)
        self.dones.append((color, delay))
        # print(t1 - t0)
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
        dbprint('deleting')
        self.stop()
        self.ser.close()
