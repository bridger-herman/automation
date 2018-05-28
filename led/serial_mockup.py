import serial
import io

class SerialMockup:
    def __init__(self, db=False):
        self.db = db
        if self.db:
            print('Using SerialMockup')
        self.buf = io.BytesIO()
        self.format_str = '\x1b[38;2;{};{};{}m{}\x1b[0m'

    def write(self, byte):
        color = list(byte)
        rgb = color[1:4]
        white = [color[4]]*3
        self.buf.write(bytes(byte))
        print(self.format_str.format(*rgb, '#'*80))
        print(self.format_str.format(*white, '#'*80))
        print()
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
