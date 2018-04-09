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
        self.num_colors = len(color1)
        self.update_props(color1, color2, duration, resolution)
        super().__init__(serial_wrapper, white)

    def update_props(self, color1, color2, duration, resolution):
        self.start_color = color1
        self.end_color = color2
        self.duration = duration
        self.resolution = resolution
        self.setup()

    def setup(self):
        color_diff = [self.end_color[i] - self.start_color[i] \
                for i in range(self.num_colors)]
        color_step = [d/(self.resolution - 1) for d in color_diff]
        self.delays = iter([self.duration/self.resolution]*self.resolution)
        self.colors = iter([[int(self.start_color[i] + n*color_step[i] + 0.5) \
                for i in range(self.num_colors)] for n in range(self.resolution)])

if __name__ == '__main__':
    from serial_wrapper import SerialMockup, SerialWrapper
    l = LEDLinearFade(SerialWrapper('/dev/tty.usbmodem1411'), \
            (255, 0, 130), \
            (255, 25, 0), \
            5, 50, white=50)
    l.start()
