import ctypes
import traceback
import signal
import sys
from serial_wrapper import SerialWrapper

dbprint = print if 'debug' in sys.argv else lambda *args, **kwargs: None
MAX_COLORS = 4

import time

class LEDChanger:
    def __init__(self, serial_wrapper, white=None):
        self.queue = [([0, 0, 0, 0], 0.1)] # Clear out stale bits (?)
        self.dones = []
        self.white = white
        self.ser = serial_wrapper
        signal.signal(signal.SIGALRM, self._handler)
        signal.signal(signal.SIGINT, self._shutdown)
        self.active = False

    def setup(self):
        # Generators for indefinite color
        self.colors = iter([])
        self.delays = iter([])

    def _handler(self, signum, frame):
        dbprint('handled!')
        io_delay = 0
        try:
            if self.ser.inWaiting() > 0:
                t0 = time.time()
                incoming = self.ser.readline()
                t1 = time.time()
                io_delay = t1 - t0
                dbprint('readline', incoming)
            next_color = next(self.colors)
            next_delay = next(self.delays)
            self.queue.insert(0, (next_color, next_delay))
            dbprint('queuing', next_color, next_delay)
        except StopIteration:
            self.stop()
        else:
            self._send(io_delay)

    def _send(self, io_time=0):
        color, delay = self.queue.pop()
        if self.white != None:
            color += [self.white]
        color = list(color)
        dbprint('sending', color, delay)
        bytes_send = (ctypes.c_ubyte * len(color))(*color)
        t0 = time.time()
        self.ser.write(bytes_send)
        t1 = time.time()
        io_time += t1 - t0
        dbprint('sent', color, delay)
        self.dones.append((color, delay))
        io_time = io_time if (delay - io_time) >= 0 else -delay
        signal.setitimer(signal.ITIMER_REAL, delay - io_time)

    def _shutdown(self, signum, frame):
        self.stop()

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
