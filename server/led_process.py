from multiprocessing import Process

class LEDProcess(Process):
    def __init__(self, led_obj):
        self.led_obj = led_obj
        self.started = False
        print('reset process', self.led_obj.prev_color)
        super().__init__(target=self.led_obj.start)

    def start(self):
        self.started = True
        print('started LEDs', self.led_obj.prev_color)
        super().start()
        print('stopped LEDs', self.led_obj.prev_color)
