from led_changer import LEDChanger

class LEDSingle(LEDChanger):
    def __init__(self, serial_wrapper, color=(0, 0, 0, 0), white=None):
        super().__init__(serial_wrapper, white)
        self.delays = iter([0.1])
        self.colors = iter([color])

    def set_color(self, color):
        self.colors = iter([color])

if __name__ == '__main__':
    from serial_wrapper import SerialMockup, SerialWrapper
    l = LEDSingle(SerialWrapper('/dev/tty.usbmodem1411'), \
            (255, 0, 130, 0))
    l.start()
