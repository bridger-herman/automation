import sys
import json
import time
from led_process import LEDProcess
from multiprocessing import Process
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
        self.led_obj = LEDGradient(self.ser, "./gradients/test.png", 2, False)
        self._set_led_process()
        super().__init__((address, port), partial(Handler, self._get_routes()))

    def _get_routes(self):
        return {
            ''            :(('GET', 'POST'), self.index),
            'get-gradient':(('GET'), self.get_gradient),
            'set-gradient':(('POST'), self.set_gradient),
            'playing'     :(('GET'), self.playing),
            'toggle-play' :(('POST'), self.toggle_play),
        }

    def _set_led_process(self):
        self.led_process = LEDProcess(self.led_obj)

    def _active(self):
        # return self.led_process.started and self.led_process.exitcode not None
        return self.led_process.is_alive()

    def toggle_play(self, data=''):
        resp = (True, '', '')
        if self.led_process.exitcode is not None:  # Reset, then start again
            self._set_led_process()
        if not self.led_process.started:  # We're ready to start
            self.led_process.start()
            return resp
        #  else:  # LEDs currently going
        self.led_process.terminate()
        self._set_led_process()
        return resp

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
        print('playing:', self._active())
        return (True, '', json.dumps({'playing':self._active()}))

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
    httpd = LEDServer('0.0.0.0', 8000, '/dev/ttyACM1')
    httpd.serve_forever()
