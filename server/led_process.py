from multiprocessing import Process

class LEDProcess(Process):
    def __init__(self, led_obj):
        self.led_obj = led_obj
        self.started = False
        super().__init__(target=self.led_obj.start)

    def start(self):
        self.started = True
        super().start()
