from led_changer import LEDChanger
from PIL import Image
import numpy as np
import traceback
from color_manager import read_col

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
        self.num_colors = 4
        self.gradient = None
        self.gradient_file = gradient_file
        self.brightness = 1.0
        self.update_props(gradient_file, duration, loop)

    def update_props(self, gradient_file, duration, loop, brightness=1.0):
        if gradient_file != self.gradient_file:
            self.gradient = None
        self.brightness = brightness
        self.gradient_file = gradient_file
        self.duration = duration
        self.loop = loop
        self.setup()

    def setup(self):
        colors_full_res = self._load_from_file()
        for cutoff, divisor in PERFORMANCE_CUTOFFS:
            if self.duration <= cutoff:
                colors_full_res = colors_full_res[::divisor]
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

    def _inf_gen(self, lst):
        while True:
            for item in lst:
                yield item

    def _load_from_file(self):
        print('loading from file')
        self.gradient = load_gradient(self.gradient_file)
        try:
            start_color = read_col()
        except:
            traceback.print_exc()
            start_color = [255, 255, 255, 255]
        print('evaled color', start_color)
        self.gradient = [[int(self.brightness * c) for c in rgbw] for rgbw in self.gradient]
        end_color = self.gradient[0]

        # Fade between colors should last half a second
        resolution = (self.duration / len(self.gradient))
        assert resolution > 0
        resolution = int(1.0 / resolution)

        num_colors = len(start_color)
        color_diff = [(end_color[i] - start_color[i]) \
                for i in range(num_colors)]
        color_step = [d/resolution for d in color_diff]
        fading_colors = list(iter([[int(start_color[i] + n*color_step[i] + 0.5) \
                for i in range(num_colors)] for n in range(resolution)]))
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
    return [list(pixels[mid_rgb, i, :]) + [pixels[mid_white, i, 2]] \
            for i in range(cols)]

def solid_color(gradient_pixels, color_tolerance=1):
    colors = zip(*gradient_pixels)
    collapsed_colors = [set(c) for c in colors]
    if all([len(c) <= color_tolerance for c in collapsed_colors]):
        return [tuple(c)[0] for c in collapsed_colors]
    else:
        return None

def main():
    from serial_wrapper import SerialWrapper
    l = LEDGradient(
            SerialWrapper('/dev/ttyACM0'),
            '../server/gradients/grad_04_sunrise.png',
            duration=10,
            loop=False
    )
    l.start()

if __name__ == '__main__':
    main()
