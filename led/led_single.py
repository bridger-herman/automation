from led_changer import LEDChanger

class SingleLED(LEDChanger):
    def __init__(self, serial_wrapper, color=(0, 0, 0, 0), white=None):
        #  if len(color) != 4 and white == None:
            #  raise ValueError('Must have white channel')
        super().__init__(serial_wrapper, white)
        self.delays = iter([0.1])
        self.colors = iter([color])
        self._verify()

    def set_color(self, color):
        self.colors = iter([color])

if __name__ == '__main__':
    s = SingleLED((255, 0, 100, 0))
    s.start()
