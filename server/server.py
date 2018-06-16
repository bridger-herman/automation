import os
import sys
import json
import time
import traceback
from led_process import LEDProcess
from http.server import HTTPServer
from functools import partial
from pathlib import Path

sys.path.append('../led')
from led_gradient import LEDGradient, load_gradient, solid_color
from led_fade import LEDLinearFade
from serial_wrapper import SerialWrapper
from handler import Handler

class LEDServer(HTTPServer):
    def __init__(self, address, port, arduino=None):
        print('initializing server', address, port)
        self.ser = SerialWrapper(arduino)
        self.which_gradient = 0
        self.led_obj = LEDGradient(
                self.ser,
                self._get_gradient_list()[self.which_gradient],
                2,
                False
        )
        self._set_led_process()
        super().__init__((address, port), partial(Handler, self._get_routes()))

    def _get_routes(self):
        return {
            ''            :(('GET', 'POST'), self.index),
            'get-gradient':(('GET'), self.get_gradient),
            'set-gradient':(('POST'), self.set_gradient),
            'is-playing'     :(('GET'), self.is_playing),
            'toggle-play' :(('POST'), self.toggle_play),
            'gradient-list':(('GET'), self.gradient_list),
        }

    def _set_led_process(self):
        print('before setting process', self.led_obj.prev_color)
        self.led_process = LEDProcess(self.led_obj)

    def _active(self):
        return self.led_process.is_alive()

    def _get_gradient_list(self):
        grad_dir = Path('./gradients')
        return list(sorted(map(lambda g: str(grad_dir.joinpath(g)), \
                os.listdir(str(grad_dir)))))

    def gradient_list(self, data=''):
        gradients = self._get_gradient_list()
        return (True, 'application/json', json.dumps({'gradients':gradients}))

    def toggle_play(self, data=''):
        if not self._active():  # Reset, then start again
            self._set_led_process()
        if not self.led_process.started:  # We're ready to start
            print('starting process', self.led_obj.prev_color)
            self.led_process.start()
        else:
            print('terminating process', self.led_obj.prev_color)
            self.led_process.terminate()
            print('terminated process', self.led_obj.prev_color)
            self._set_led_process()
        return (True, '', '')

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
        print('beginning of get_gradient', self.led_obj.prev_color)
        to_send = {
            'duration':self.led_obj.duration,
            'loop':self.led_obj.loop,
            'src':self.led_obj.gradient_file,
            'which':self.which_gradient,
        }
        return (True, '', json.dumps(to_send))

    def is_playing(self, data=''):
        print('is playing', self.led_obj.prev_color, id(self.led_obj.prev_color))
        return (True, '', json.dumps({'playing':self._active()}))

    def set_gradient(self, data=''):
        print('beginning of set_gradient', self.led_obj.prev_color)
        try:
            request = json.loads(data.decode('utf-8'))
            loop = bool(request['loop'])
            duration = float(request['duration'])
            self.which_gradient = int(request['which'])
            src = self._get_gradient_list()[self.which_gradient]
            print('before update props', self.led_obj.prev_color)
            self.led_obj.update_props(src, duration, loop)
            print('after update props', self.led_obj.prev_color)
            return (True, '', '')
        except:
            traceback.print_exc()
            return (False, 'text/plain', 'Failure')

if __name__ == '__main__':
    httpd = LEDServer('0.0.0.0', 8000, '/dev/ttyACM0')
    httpd.serve_forever()
