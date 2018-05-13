import sys
import json
from http.server import HTTPServer
from functools import partial

sys.path.append('../led')
from led_gradient import LEDGradient
from serial_wrapper import SerialWrapper
from handler import Handler

class LEDServer(HTTPServer):
    def __init__(self, address, port, arduino=None):
        print('initializing server', address, port)
        self.ser = SerialWrapper(arduino)
        self.led_obj = LEDGradient(self.ser, "./static/gradients/test.png", 5, False)
        super().__init__((address, port), partial(Handler, self._get_routes()))

    def _get_routes(self):
        return {
            ''             :(('GET', 'POST'), self.index),
            'get-gradient' :(('GET'), self.get_gradient),
            'set-gradient':(('POST'), self.set_gradient),
            'playing'     :(('GET'), self.playing),
            'toggle-play' :(('POST'), self.toggle_play),
        }

    # Takes string as data
    # returns triple (success:bool, result_type:string, result)
    # result type will be application/json if blank
    def index(self, data=''):
        try:
            ind = open('index.html')
            text = ind.read()
            ind.close()
            return (True, 'text/html', text)
        except:
            return (False, 'text/html', 'Failed to load')

    def get_gradient(self, data=''):
        to_send = {
            'duration':self.led_obj.duration,
            'loop':self.led_obj.loop,
            'src':self.led_obj.gradient_file,
        }
        return (True, '', json.dumps(to_send))

    def playing(self, data=''):
        return (True, '', json.dumps({'playing':self.led_obj.active}))

    def toggle_play(self, data=''):
        if not self.led_obj.active:
            self.led_obj.start()
        else:
            self.led_obj.stop()
        return (True, '', '')

    def set_gradient(self, data=''):
        try:
            request = json.loads(data)
            loop = bool(request['loop'])
            duration = float(request['duration'])
            src = request['src']
            self.led_obj.update_props(src, duration, loop)
            return (True, '', '')
        except:
            print('error!')
            return (False, 'text/plain', 'Failure')

if __name__ == '__main__':
    httpd = LEDServer('localhost', 8000, '/dev/ttyACM0')
    httpd.serve_forever()
