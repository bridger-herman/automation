from led_changer import SerialLEDChanger

class SingleLED(SerialLEDChanger):
    def __init__(self, color=(0, 0, 0, 0), delay=1000, alpha=None):
        if len(color) != 4 and alpha == None:
            raise ValueError('Must have alpha channel')
        super().__init__(alpha)
        self.delays = self.__inf_value(delay)
        self.colors = self.__inf_value(color)

    def __inf_value(self, value):
        while True:
            yield value 

if __name__ == '__main__':
    s = SingleLED((255, 255, 255, 255))
    s.start()
