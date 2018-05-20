from led_changer import LEDChanger
from cv2 import imread
from serial_wrapper import SerialMockup, SerialWrapper
import pickle
import sys
import os

# Performance optimization, hopefully not necissary because it looks
# super crappy
# PERFORMANCE_CUTOFFS = [
#     (15,2),
#     (10,4),
# ]

class LEDGradient(LEDChanger):
    def __init__(self, serial_wrapper, gradient_file, duration=10, loop=True):
        '''
        Class LEDGradient
        Attributes:
            serial_wrapper: SerialWrapper object
            gradient_file: image file with RGB and white gradients
            duration: How long to fade through the gradient
            loop: Should we go back to the beginning once we're through
        '''
        super().__init__(serial_wrapper, None)
        self.num_colors = 4
        self.gradient = None
        self.update_props(gradient_file, duration, loop)

    def update_props(self, gradient_file, duration, loop):
        self.gradient_file = gradient_file
        self.duration = duration
        self.loop = loop
        self.setup()

    def setup(self):
        colors_full_res = self._load_from_file()
        # for cutoff, divisor in PERFORMANCE_CUTOFFS:
        #     if self.duration <= cutoff:
        #         colors_full_res = colors_full_res[::divisor]
        time_res = self.duration/len(colors_full_res)
        delays = [time_res for _ in range(len(colors_full_res))]
        if self.loop:
            self.colors = self._inf_gen(colors_full_res)
            self.delays = self._inf_gen(delays)
        else:
            self.colors = iter(colors_full_res)
            self.delays = iter(delays)
        print('time-res:', time_res)
        print('duration:', self.duration)
        print('loop:', self.loop)

    def _inf_gen(self, lst):
        while True:
            for item in lst:
                yield item

    def _load_from_file(self):
        if self.gradient is None:
            print('loading from file')
            pixels = imread(self.gradient_file)
            pixels = pixels[:, :, ::-1] # BGR to RGB
            rows, cols, depth = pixels.shape
            assert depth == 3
            mid = rows//2
            mid_rgb = mid//2
            mid_white = mid_rgb + mid
            self.gradient = [list(pixels[mid_rgb, i, :]) + [pixels[mid_white, i, 2]] \
                    for i in range(cols)]
        return self.gradient
