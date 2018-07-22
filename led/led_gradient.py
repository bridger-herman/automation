from led_changer import LEDChanger
from PIL import Image
import numpy as np
from scipy import ndimage
import traceback

PERFORMANCE_CUTOFFS = [
    (15,2),
    (6,4),
]

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
        brightness_img = make_brightness_gradient(self.prev_color)
        brightness_img.save('./brightness_slider.png')
        self.num_colors = 4
        self.gradient = None
        self.gradient_file = gradient_file
        self.need_cleanup = False
        self.num_fade_colors = 0
        self.divisor = 1
        self.brightness = 1.0

        self.update_props(gradient_file, duration, loop)

    def update_resolution(self):
        # Fade between colors/gradients will last 1.0 second
        resolution = self.duration / (len(self.gradient) // self.divisor)
        assert resolution > 0
        self.resolution = int(2.0 / resolution)

    def update_props(self, gradient_file, duration, loop, brightness=1.0):
        if gradient_file != self.gradient_file or brightness != self.brightness:
            self.gradient = None
        self.brightness = brightness
        self.gradient_file = gradient_file
        self.duration = duration
        self.loop = loop
        self.setup()

    def setup(self):
        for cutoff, divisor in PERFORMANCE_CUTOFFS:
            if self.duration <= cutoff:
                self.divisor = divisor
        colors_full_res = self._load_from_file()
        colors_full_res = colors_full_res[::self.divisor]
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
        print('brightness:', self.brightness)

    # Pop off the colors from fading between
    def cleanup(self):
        if not self.need_cleanup:
            return
        for i in range(self.num_fade_colors//self.divisor):
            c = next(self.colors)
            d = next(self.delays)
        self.need_cleanup = False

    def _inf_gen(self, lst):
        first_run = True
        while True:
            for item in lst:
                yield item
            if first_run:
                lst = lst[self.num_fade_colors//self.divisor:]
                first_run = False

    def set_previous_color(self):
        super().set_previous_color()
        brightness_compensation = 0 if self.brightness == 0 else 1.0/self.brightness
        compensated_color = [int(brightness_compensation * c) for c in self.prev_color]
        brightness_img = make_brightness_gradient(compensated_color)
        brightness_img.save('./brightness_slider.png')

    def _load_from_file(self):
        print('loading from file')
        self.gradient = load_gradient(self.gradient_file)
        self.need_cleanup = True
        try:
            start_color = self.prev_color
        except:
            traceback.print_exc()
            start_color = [255, 255, 255, 255]
        print('evaled color', start_color)
        # TODO: load from file when updating props and brightness changes
        self.gradient = [[int(self.brightness * c) for c in rgbw] for rgbw in self.gradient]
        end_color = self.gradient[0]

        self.update_resolution()

        num_colors = len(start_color)
        color_diff = [(end_color[i] - start_color[i]) \
                for i in range(num_colors)]
        color_step = [d/self.resolution for d in color_diff]
        fading_colors = list(iter([[int(start_color[i] + n*color_step[i] + 0.5) \
                for i in range(num_colors)] for n in range(self.resolution)]))
        self.num_fade_colors = len(fading_colors)
        self.gradient = fading_colors + self.gradient
        return self.gradient

def load_gradient(filename):
    img = Image.open(filename)
    pixels = np.array(img, dtype=np.uint8)
    rows, cols, depth = pixels.shape
    assert depth == 3
    mid = rows//2
    mid_rgb = mid//2
    mid_white = mid_rgb + mid
    gradient_pixels = np.array([list(pixels[mid_rgb, i, :]) + [pixels[mid_white, i, 2]] \
            for i in range(cols)])
    gradient_pixels = ndimage.generic_filter(gradient_pixels,
            lambda val: 0 if val <= 1 else val, 1)
    gradient_pixels = ndimage.median_filter(gradient_pixels, (51, 1))
    return list(gradient_pixels)

def solid_color(gradient_pixels, color_tolerance=1):
    colors = zip(*gradient_pixels)
    collapsed_colors = [set(c) for c in colors]
    if all([len(c) <= color_tolerance for c in collapsed_colors]):
        return [tuple(c)[0] for c in collapsed_colors]
    else:
        return None

# Also using this to save the current color for use in brightness slider
# Interpolate from black -> c
def make_brightness_gradient(end_color):
    start_color = [0, 0, 0]

    width = 1024
    height = 50

    num_colors = len(start_color)
    color_diff = [(end_color[i] - start_color[i]) \
            for i in range(num_colors)]
    color_step = [d/width for d in color_diff]
    fading_colors = [[[int(start_color[i] + c*color_step[i] + 0.5) \
            for i in range(num_colors)] for c in range(width)] for r in range(height)]

    return Image.fromarray(np.asarray(fading_colors, dtype=np.uint8), mode='RGB')
