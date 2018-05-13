import sys
sys.path.append('../led')
from led_single import LEDSingle
from led_fade import LEDLinearFade
from led_gradient import LEDGradient
from serial_wrapper import SerialWrapper, SerialMockup
from flask import Flask, render_template, request, jsonify

DEBUG = False

def rgbw_to_hex(r, g, b, w):
    return ('#' + '{:>02}'*4).format(*map(lambda v: v[2:], [hex(r), hex(g), hex(b), hex(w)]))

class HomeServer:
    def __init__(self, host=None, arduino=None):
        self.ser = SerialWrapper(arduino, db=DEBUG) if arduino is not \
                None else SerialMockup(db=DEBUG)
        self.host = host
        self.app = Flask(__name__)
        self.current_color = [0, 0, 0, 0]
        # self.led_obj = LEDLinearFade(self.ser, self.current_color, \
        #         self.current_color, 1, 30)
        self.led_obj = LEDGradient(self.ser, "./static/gradients/test.png")
        self._setup_routes()

    def _setup_routes(self):
        self.app.route('/', methods=['GET', 'POST'])(self.index)
        self.app.route('/update-leds', methods=['POST'])(self.update_leds)
        self.app.route('/gradient-info', methods=['GET'])(self.gradient_info)

    def update_leds(self):
        try:
            rgbw = request.json['rgbw']
            assert len(rgbw) == 4
            hx = rgbw_to_hex(*rgbw)
            if not self.led_obj.active:
                print(hx)
                self.led_obj.update_props(self.current_color, rgbw, 1, 30)
                self.led_obj.start()
                self.current_color = rgbw
            return jsonify({'status':200})
        except KeyError:
            return jsonify({'status':400})
        except AssertionError:
            return jsonify({'status':400})

    def gradient_info(self):
        to_send = {
            'duration':self.led_obj.duration,
            'loop':self.led_obj.loop,
            'src':self.led_obj.gradient_file,
            'status':200
        }
        return jsonify(to_send)

    def index(self):
        return render_template('index.html', \
                wheel_color_value=rgbw_to_hex(*self.current_color))

    def run(self):
        if self.host is None:
            self.app.run()
        else:
            self.app.run(host=self.host)

if __name__ == "__main__":
    server_args = [sys.argv[i] if i < len(sys.argv) else None for i in range(1, 3)]
    s = HomeServer(*server_args)
    s.run()
