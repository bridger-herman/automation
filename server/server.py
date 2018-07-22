import os
import sys
import json
import traceback
from http.server import HTTPServer
from functools import partial
from pathlib import Path
from datetime import datetime

sys.path.append('../led')
from led_gradient import LEDGradient, load_gradient, solid_color
from led_fade import LEDLinearFade
from serial_wrapper import SerialWrapper
from handler import Handler
from alarm import Alarm

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
        self._set_alarm_list()
        super().__init__((address, port), partial(Handler, self._get_routes()))

    def _get_routes(self):
        return {
            ''            :(('GET', 'POST'), self.index),
            'get-gradient':(('GET'), self.get_gradient),
            'set-gradient':(('POST'), self.set_gradient),
            'is-playing'     :(('GET'), self.is_playing),
            'play-leds' :(('POST'), self.play_leds),
            'stop-leds' :(('POST'), self.stop_leds),
            'gradient-list':(('GET'), self.gradient_list),
            'alarm-list':(('GET', 'POST'), self.alarm_list),
        }

    def _set_alarm_list(self):
        alarms_text = self._get_alarm_list()
        self.alarms = []
        for alarm in alarms_text:
            alarm_time = datetime(
                year=alarm['year'],
                month=alarm['month'],
                day=alarm['day'],
                hour=alarm['hour'],
                minute=alarm['minute'],
                second=alarm['second'],
            )
            if datetime.now() < alarm_time:
                self.alarms.append(Alarm(alarm_time, self._play_leds_from_alarm,
                        (alarm['src'], alarm['duration'], alarm['loop'])
                ))

    def _play_leds_from_alarm(self, src, duration, loop):
        self.led_obj.update_props(src, duration, loop)
        self.play_leds()

    def _get_alarm_list(self):
        fin = open('./alarm_list.csv')
        alarm_list = []
        for line in fin:
            line = line.split(',')
            alarm_list.append({
                'year': int(line[0]),
                'month': int(line[1]),
                'day': int(line[2]),
                'hour': int(line[3]),
                'minute': int(line[4]),
                'second': int(line[5]),
                'src': line[6],
                'duration': int(line[7]),
                'loop': bool(eval(line[8])),
            })
        return alarm_list

    def alarm_list(self, data=''):
        if len(data) > 0:
            self._set_alarm_list()
        try:
            alarm_list = self._get_alarm_list()
            return (True, 'application/json', json.dumps({'alarms': alarm_list}))
        except:
            return (False, 'application/json', json.dumps({}))

    def _get_gradient_list(self):
        grad_dir = Path('./gradients')
        return list(sorted(map(lambda g: str(grad_dir.joinpath(g)), \
                os.listdir(str(grad_dir)))))

    def gradient_list(self, data=''):
        gradients = self._get_gradient_list()
        return (True, 'application/json', json.dumps({'gradients':gradients}))

    def play_leds(self, data=''):
        if not self.led_obj.active:
            self.led_obj.start()
        return (True, '', '')

    def stop_leds(self, data=''):
        if self.led_obj.active:
            self.led_obj.stop()
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
        to_send = {
            'duration':self.led_obj.duration,
            'loop':self.led_obj.loop,
            'src':self.led_obj.gradient_file,
            'which':self.which_gradient,
            'brightness':self.led_obj.brightness,
        }
        return (True, '', json.dumps(to_send))

    def is_playing(self, data=''):
        return (True, '', json.dumps({'playing':self.led_obj.active}))

    def set_gradient(self, data=''):
        if self.led_obj.active:
            return (True, '', '')
        try:
            request = json.loads(data.decode('utf-8'))
            loop = bool(request['loop'])
            duration = float(request['duration'])
            self.which_gradient = int(request['which'])
            src = self._get_gradient_list()[self.which_gradient]
            brightness = float(request['brightness'])
            self.led_obj.update_props(src, duration, loop, brightness)
            return (True, '', '')
        except:
            traceback.print_exc()
            return (False, 'text/plain', 'Failure')

if __name__ == '__main__':
    httpd = LEDServer('0.0.0.0', 8000, '/dev/ttyACM0')
    httpd.serve_forever()
