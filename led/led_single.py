from led_changer import LEDChanger

class SingleLED(LEDChanger):
    def __init__(self, serial_wrapper, color=(0, 0, 0, 0), alpha=None):
        if len(color) != 4 and alpha == None:
            raise ValueError('Must have alpha channel')
        super().__init__(serial_wrapper, alpha)
        self.delays = iter([0.1])
        self.colors = iter([color])

    def set_color(self, color):
        self.colors = iter([color])

if __name__ == '__main__':
    s = SingleLED((255, 0, 100, 0))
    s.start()
