import sys
sys.path.append('../led')
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from led_gradient import LEDGradient
from serial_wrapper import SerialWrapper, SerialMockup
from io import BytesIO
from functools import partial
import mimetypes
import json

ENCODING = 'utf-8'
DEFAULT_CONTENT = 'application/json'

class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.routes = args[0]
        super().__init__(*(args[1:]), **kwargs)

    def _send_failure(self, status=400, msg='Failure'):
        self._send_hdr(status, 'text/plain')
        self.wfile.write(bytes(msg, ENCODING))

    def _send_hdr(self, status, type):
        self.send_response(status)
        self.send_header('content-type', type)
        self.end_headers()

    def do_GET(self):
        self.path = self.path[1:] # Discard leading slash
        content_length = self.headers['Content-Length']
        if content_length != None:
            data = self.rfile.read(int(content_length))
        else:
            data = ''
        if self.path in self.routes:
            types, route_fn = self.routes[self.path]
            if 'GET' not in types:
                return
            success, content_type, response = route_fn(data)
            content_type = DEFAULT_CONTENT if content_type == '' else content_type
            if not success:
                self._send_failure()
            else:
                self._send_hdr(200, content_type)
                self.wfile.write(bytes(response, ENCODING))
        else:
            try:
                fout = open(self.path, 'rb')
                self._send_hdr(200, mimetypes.guess_type(self.path))
                self.wfile.write(fout.read())
                fout.close()
            except FileNotFoundError:
                self._send_failure(404, 'File not found')
            except:
                self._send_failure()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        if content_length != None:
            data = self.rfile.read(int(content_length))
        else:
            data = ''
        if self.path in self.routes:
            types, route_fn = self.routes[self.path]
            if 'POST' not in types:
                return
            success, content_type, response = route_fn(data)
            content_type = DEFAULT_CONTENT if content_type == '' else content_type
            if not success:
                self._send_failure()
            else:
                self._send_hdr(200, content_type)
                self.wfile.write(bytes(response, ENCODING))
        # self.send_response(200)
        # self.send_header('content-type', 'application/json')
        # self.end_headers()
        # print('body', body)
        # response = BytesIO()
        # response.write(b'This is POST request. ')
        # response.write(b'Received: ')
        # response.write(body)
        # self.wfile.write(bytes(json.dumps({'hello':'world'}), 'utf-8'))
        # self.wfile.write(response.getvalue())

class LEDServer(HTTPServer):
    def __init__(self, address, port, arduino=None):
        print('initializing server', address, port)
        self.ser = SerialWrapper(arduino)
        self.led_obj = LEDGradient(self.ser, "./static/gradients/test.png", 5)
        super().__init__((address, port), partial(Handler, self._get_routes()))

    def _get_routes(self):
        return {
            ''             :(('GET', 'POST'), self.index),
            'get-gradient' :(('GET'), self.get_gradient),
            'set-gradient':(('POST'), self.set_gradient),
            'playing'     :(('GET'), self.playing),
            'toggle-play' :(('POST'), self.toggle_play),
        }

        # self.app.route('/', methods=['GET', 'POST'])(self.index)
        # self.app.route('/update-leds', methods=['POST'])(self.update_leds)
        # self.app.route('/get-gradient', methods=['GET'])(self.get_gradient)
        # self.app.route('/set-gradient', methods=['POST'])(self.set_gradient)
        # self.app.route('/playing', methods=['GET'])(self.playing)
        # self.app.route('/toggle-play', methods=['POST'])(self.toggle_play)

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
    httpd = LEDServer('localhost', 8000)
    httpd.serve_forever()
