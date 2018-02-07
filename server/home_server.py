import sys
sys.path.append('../led')
from led_single import LEDSingle
from led_fade import LEDLinearFade
from serial_wrapper import SerialWrapper, SerialMockup
from flask import Flask, render_template, request, jsonify

def rgbw_to_hex(r, g, b, w):
    return '#{:>02}{:>02}{:>02}{:>02}'.format(*map(lambda v: v[2:], [hex(r), hex(g), hex(b), hex(w)]))

class HomeServer:
    def __init__(self, host=None, arduino=None):
        self.ser = SerialWrapper(arduino) if arduino is not None else SerialMockup(db=False)
        self.host = host
        self.app = Flask(__name__)
        self.current_color = [0, 0, 0, 0]
        self.led_obj = LEDLinearFade(self.ser, self.current_color, self.current_color, 1, 10)
        self._setup_routes()

    def _setup_routes(self):
        self.app.route('/', methods=['GET', 'POST'])(self.index)
        self.app.route('/update-leds', methods=['POST'])(self.update_leds)

    def update_leds(self):
        try:
            rgbw = request.json['rgbw']
            assert len(rgbw) == 4
            self.current_color = rgbw
            hx = rgbw_to_hex(*rgbw)
            print(hx)
            self.led_obj.__init__(self.ser, self.current_color, rgbw, 1, 30)
            self.led_obj.start()
            return jsonify({'status':200})
        except KeyError:
            return jsonify({'status':400})
        except AssertionError:
            return jsonify({'status':400})


    def index(self):
        return render_template('index.html', wheel_color_value=rgbw_to_hex(*self.current_color))

    def run(self):
        if self.host is None:
            self.app.run()
        else:
            self.app.run(host=self.host)

if __name__ == "__main__":
    server_args = [sys.argv[i] if i < len(sys.argv) else None for i in range(1, 3)]
    s = HomeServer(*server_args)
    s.run()
