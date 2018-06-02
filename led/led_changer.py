import ctypes
import traceback
import signal
import sys
import time
from serial_wrapper import SerialWrapper
from threading import Timer

dbprint = print if 'debug' in sys.argv else lambda *args, **kwargs: None
MAX_COLORS = 4

import time

class LEDChanger:
    def __init__(self, serial_wrapper, white=None):
        self.queue = []
        self.dones = []
        self.white = white
        self.start_time = time.time()
        self.ser = serial_wrapper
        self.timer = None # Don't start timing until start() is called
        signal.signal(signal.SIGTERM, self._shutdown)
        self.active = False

    def setup(self):
        # Generators for indefinite color
        self.colors = iter([])
        self.delays = iter([])

    def _handler(self):
        dbprint('handled!')
        io_delay = 0
        t0 = time.time()
        # print('befpre read')
        incoming = self.ser.readline()
        # print('after read')
        t1 = time.time()
        io_delay = t1 - t0
        try:
            next_color = next(self.colors)
            next_delay = next(self.delays)
            self.queue.insert(0, (next_color, next_delay))
            dbprint('queuing', next_color, next_delay)
        except StopIteration:
            self.stop()
        else:
            self._send(io_delay)

    def _send(self, io_time=0):
        if len(self.queue) == 0:
            return
        color, delay = self.queue.pop()
        if self.white != None:
            color += [self.white]
        data = [0] + list(color) # [<reset>, <color>]
        dbprint('sending', color)
        bytes_send = (ctypes.c_ubyte * len(data))(*data)
        t0 = time.time()
        self.ser.write(bytes_send)
        t1 = time.time()
        io_time += t1 - t0
        dbprint('sent', color, delay)
        self.dones.append((color, delay))
        io_time = io_time if (delay - io_time) >= 0 else -delay
        self.timer = Timer(delay - io_time, self._handler)
        self.timer.start()

    def _shutdown(self, signum, frame):
        print('caught SIGTERM')
        self.stop()

    def start(self):
        print('started')
        self.active = True
        self.start_time = time.time()
        self._handler()
        # Spin until we're done here
        while self.active:
            time.sleep(0.001)
        print('past loop')

    def stop(self):
        if not self.active:
            return
        dbprint('stopped')
        self.active = False
        while len(self.queue) > 0:
            dbprint('finishing send')
            self._send()
        bytes_send = (ctypes.c_ubyte * 5)(*[1, 0, 0, 0, 0])
        self.ser.write(bytes_send)
        print('total time', time.time() - self.start_time)
        self.reset()

    def reset(self):
        print('leds resetting')
        try:
            colors, delays = zip(*self.dones)
            self.colors = iter(colors)
            self.delays = iter(delays)
            self.dones = []
        except ValueError:
            print('nothing to reset')


    def __del__(self):
        dbprint('deleting')
        self.stop()
        self.ser.close()
        self.timer = None
