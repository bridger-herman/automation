import sys
sys.path.append('../led')
from led_single import SingleLED
from led_fade import LEDLinearFade
from serial_wrapper import SerialWrapper, SerialMockup
from flask import Flask, render_template, request

class HomeServer:
    def __init__(self, host=None):
        self.ser = SerialMockup(db=False)
        self.host = host
        self.app = Flask(__name__)
        self.current_color = [0, 0, 0, 0]
        self.led_obj = LEDLinearFade(self.ser, self.current_color, self.current_color, 1, 10)
        self._setup_routes()

    def _setup_routes(self):
        self.app.route('/', methods=['GET', 'POST'])(self.index)

    def index(self):
        if len(request.form) > 0:
            led_vals = [int(v) for k, v in request.form.items()]
            self.led_obj.__init__(self.ser, self.current_color, led_vals, 1, 30)
            self.led_obj.start()
            self.current_color = led_vals
            return render_template('index.html',
                    red_value=request.form['red'],
                    green_value=request.form['green'],
                    blue_value=request.form['blue'],
                    white_value=request.form['white']
            )
        else:
            return render_template('index.html')

    def run(self):
        if self.host is None:
            self.app.run()
        else:
            self.app.run(host=self.host)

if __name__ == "__main__":
    s = HomeServer()
    s.run()
