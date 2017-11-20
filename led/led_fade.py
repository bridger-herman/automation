from led_changer import LEDChanger, NUM_COLORS

class LEDLinearFade(LEDChanger):
    def __init__(self, serial_wrapper, color1=(0, 0, 0, 0), color2=(0, 0, 0, 0),
            duration=1, resolution=10, white=None):
        '''
        Class LEDFade
        Attributes:
            serial_wrapper: SerialWrapper object
            color1: RGBW start color
            color2: RGBW end color
            duration: Duration of fade, in seconds
            resolution: Resolution of fade (how many times to divide `duration` into)
        '''
        if any([len(color1) != NUM_COLORS, len(color2) != NUM_COLORS]) and white == None:
            raise ValueError('Must have white channel')
        super().__init__(serial_wrapper, white)
        self.start_color = color1
        self.end_color = color2
        self.duration = duration
        self.resolution = resolution
        self.colors, self.delays = self._get_iterators()

    def _get_iterators(self):
        color_diff = [self.end_color[i] - self.start_color[i] for i in range(NUM_COLORS)]
        color_step = [d/(self.resolution - 1) for d in color_diff]
        delays = iter([self.duration/self.resolution]*self.resolution)
        colors = iter([[int(self.start_color[i] + n*color_step[i] + 0.5) for i in range(NUM_COLORS)] for n in range(self.resolution)])
        return colors, delays

if __name__ == '__main__':
    from serial_wrapper import SerialMockup
    l = LEDLinearFade(SerialMockup(), (0, 0, 0, 0), (255, 255, 255, 255), 1, 4)
    l.start()
