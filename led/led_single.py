from led_changer import SerialLEDChanger

class SingleLED(SerialLEDChanger):
    def __init__(self, color=(0, 0, 0, 0), alpha=None):
        if len(color) != 4 and alpha == None:
            raise ValueError('Must have alpha channel')
        super().__init__(alpha)
        self.delays = iter([0.1])
        self.colors = iter([color])

if __name__ == '__main__':
    #  s = SingleLED((255, 255, 255, 255))
    #  s = SingleLED((210, 0, 113, 0))
    s = SingleLED((255, 0, 100, 0))
    s.start()
