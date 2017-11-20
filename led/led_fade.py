from led_changer import LEDChanger 

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
            resolution: Resolution of fade (how many times to divide
                    `duration` into)
            white: Constant color to use for white (if none, assuming color1
                    and color2 have white)
        '''
        super().__init__(serial_wrapper, white)
        self.start_color = color1
        self.end_color = color2
        self.duration = duration
        self.resolution = resolution
        self.colors, self.delays = self._get_iterators()
        self._verify()

    def _get_iterators(self):
        color_diff = [self.end_color[i] - self.start_color[i] \
                for i in range(self.num_colors)]
        color_step = [d/(self.resolution - 1) for d in color_diff]
        delays = iter([self.duration/self.resolution]*self.resolution)
        colors = iter([[int(self.start_color[i] + n*color_step[i] + 0.5) \
                for i in range(self.num_colors)] for n in range(self.resolution)])
        return colors, delays

if __name__ == '__main__':
    from serial_wrapper import SerialMockup
    l = LEDLinearFade(SerialMockup(), (0, 0, 0, 0), (4, 8, 4, 4), 1, 5)
    l.start()
