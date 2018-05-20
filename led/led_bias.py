from mss import mss
from color_helpers import clamp
from led_changer import LEDChanger
import numpy as np
from serial_wrapper import SerialMockup, SerialWrapper

class LEDBias(LEDChanger):
    def __init__(self, serial_wrapper, brightness_multiplier=0.5,
            saturation_adjust=2.0, size=200):
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
        self.brightness_multiplier = brightness_multiplier
        self.saturation_adjust = saturation_adjust
        self.colors = self._next_color()
        self.delays = self._next_delay()

    def _next_color(self):
        while True:
            g = self.sct.grab(self.window)
            pixels = np.array(g.pixels)
            avg_color = np.average(pixels, axis=(0, 1))
            avg_color = (1/255)*np.power(avg_color, np.ones(len(avg_color))*2)
            avg_color = avg_color*self.brightness_multiplier
            avg_val = np.average(avg_color)

             # Adjust "saturation"
            adjusted = avg_val + (self.saturation_adjust*(avg_color - avg_val))

            adjusted = clamp(adjusted)
            avg = np.array(adjusted, dtype=np.uint8)
            yield list(avg)

    def _next_delay(self):
        while True:
            yield 1/30 # desired 30fps


if __name__ == '__main__':
    l = LEDBias(SerialWrapper('/dev/ttyACM0'))
    l.start()
