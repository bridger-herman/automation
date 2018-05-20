from mss import mss
from led_changer import LEDChanger
import numpy as np
# from cv2 import imread
from serial_wrapper import SerialMockup, SerialWrapper
# import pickle
# import sys
# import os
import time

class LEDBias(LEDChanger):
    def __init__(self, serial_wrapper, size=100):
        super().__init__(serial_wrapper, 0)
        self.sct = mss()
        mon = self.sct.monitors[0]
        print(mon)
        where_x = mon['width']//2
        where_y = mon['height']//2
        # Window centered on screen
        self.window = {
                'top': where_y + mon['top'] - size//2,
                'left': where_x + mon['left'] - size//2,
                'width': size,
                'height': size
        }
        self.colors = self._next_color()
        self.delays = self._next_delay()

    def _next_color(self):
        while True:
            # For now assumes only one pixel
            # t0 = time.time()
            g = self.sct.grab(self.window)
            pixels = np.array(g.pixels)
            avg = np.average(pixels, axis=(0, 1))*0.5
            avg = np.array(avg, dtype=np.uint8)
            # t1 = time.time()
            # yield list([0, 0, 0])
            yield list(avg[:3])

    def _next_delay(self):
        while True:
            yield 1/30 # desired 60fps


if __name__ == '__main__':
    l = LEDBias(SerialWrapper('/dev/ttyACM1'))
    l.start()
