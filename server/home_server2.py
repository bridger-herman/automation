from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler

from io import BytesIO
from functools import partial
import mimetypes
import json

class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        print('request', args[0])
        self.routes = args[0]
        super().__init__(*(args[1:]), **kwargs)

    def do_GET(self):
        print(self.path)
        if self.path == '/':
            self.path = '/index.html'
        self.path = self.path[1:] # Discard leading slash
        try:
            fout = open(self.path, 'rb')
            self.send_response(200)
            self.send_header('content-type', mimetypes.guess_type(self.path))
            self.end_headers()
            self.wfile.write(fout.read())
            fout.close()
        except FileNotFoundError:
            if self.path in self.routes:
                self.send_response(200)
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(self.routes[self.path](), 'utf-8'))
            else:
                self.send_response(404)
                self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

class LEDServer(HTTPServer):
    def __init__(self, address, port):
        print('initializing server', address, port)
        super().__init__((address, port), partial(Handler, self._get_routes()))

    def _get_routes(self):
        return {
            'get-gradient':self.get_gradient
        }

    def get_gradient(self):
        print('got gradient')
        return json.dumps({'hello':'world'})

if __name__ == '__main__':
    httpd = LEDServer('localhost', 8000)
    httpd.serve_forever()
