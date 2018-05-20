from mss import mss
from led_changer import LEDChanger
# from cv2 import imread
from serial_wrapper import SerialMockup, SerialWrapper
# import pickle
# import sys
# import os

class LEDBias(LEDChanger):
    def __init__(self, serial_wrapper, size=1):
        super().__init__(serial_wrapper, 0)
        self.sct = mss()
        mon = self.sct.monitors[2]
        print(mon)
        where_x = mon['width']//2
        where_y = mon['height']//2
        self.window = {
                'top': where_y + mon['top'],
                'left': where_x + mon['left'],
                'width': size,
                'height': size
        }
        self.colors = self._next_color()
        self.delays = self._next_delay()

    def _next_color(self):
        while True:
            # For now assumes only one pixel
            g = self.sct.grab(self.window)
            pix = g.pixels[0][0]
            yield list(pix)

    def _next_delay(self):
        while True:
            yield 1/30 # desired 60fps


if __name__ == '__main__':
    l = LEDBias(SerialWrapper('/dev/ttyACM1'))
    l.start()
