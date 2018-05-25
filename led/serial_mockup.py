import serial
import io
import turtle

class SerialMockup:
    def __init__(self, db=False):
        self.db = db
        if self.db:
            print('Using SerialMockup')
        self.buf = io.BytesIO()
        self.white_turtle = turtle.Turtle()
        self.rgb_turtle = turtle.Turtle()
        self.scr = self.rgb_turtle.getscreen()
        self._setup()

    def _setup(self):
        self.white_turtle.shape('square')
        self.rgb_turtle.shape('square')
        self.white_turtle.shapesize(1, 50)
        self.rgb_turtle.shapesize(1, 50)
        self.scr.colormode(255)
        self.white_turtle.goto(0, 50)
        self.rgb_turtle.goto(0, -50)

    def write(self, byte):
        color = list(byte)
        rgb = color[1:4]
        white = [color[4]]*3
        self.buf.write(bytes(byte))
        self.rgb_turtle.color(rgb)
        self.white_turtle.color(white)
        if self.db:
            print('writing', bytes(byte))

    def readline(self):
        val = self.buf.getvalue()
        line = self.buf.readline()
        if self.db:
            print(val.__repr__())
            print('reading', val)
        self.buf = io.BytesIO()
        return line

    def read(self, num_bytes):
        bytes = self.buf.read(num_bytes)
        if self.db:
            print('reading', bytes)
        return bytes

    def close(self):
        pass
