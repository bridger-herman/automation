from http.server import BaseHTTPRequestHandler
import mimetypes
import json

ENCODING = 'utf-8'
DEFAULT_CONTENT = 'application/json'
DEFAULT_RESPONSE = json.dumps({})

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
            response = DEFAULT_RESPONSE if response == '' else response
            if not success:
                self._send_failure()
            else:
                self._send_hdr(200, content_type)
                self.wfile.write(bytes(response, ENCODING))
        else:
            try:
                bad_word = '?dont_use_this'
                if bad_word in self.path:
                    index = self.path.index(bad_word)
                    self.path = self.path[:index]
                fout = open(self.path, 'rb')
                self._send_hdr(200, mimetypes.guess_type(self.path))
                self.wfile.write(fout.read())
                fout.close()
            except FileNotFoundError:
                self._send_failure(404, 'File not found')
            except:
                self._send_failure()

    def do_POST(self):
        self.path = self.path[1:] # Discard leading slash
        content_length = int(self.headers['Content-Length'])
        if content_length != None:
            data = self.rfile.read(int(content_length))
        else:
            data = ''
        if self.path in self.routes:
            types, route_fn = self.routes[self.path]
            if 'POST' not in types:
                self._send_hdr(200, 'text/plain')
                return
            success, content_type, response = route_fn(data)
            content_type = DEFAULT_CONTENT if content_type == '' else content_type
            response = DEFAULT_RESPONSE if response == '' else response
            if not success:
                self._send_failure()
            else:
                self._send_hdr(200, content_type)
                self.wfile.write(bytes(response, ENCODING))
        else:
            self._send_hdr(200, 'text/plain')
