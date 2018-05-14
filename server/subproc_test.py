import sys
from pathlib import Path
from subprocess import Popen, PIPE
import signal

sys.path.append('../led')

class Wrapper:
    def __init__(self):
        self.child = Popen([sys.executable, '../led/led_gradient.py'])
        signal.signal(signal.SIGINT, self._shutdown)
        self.child.communicate()

    def _shutdown(self, signum, frame):
        self.child.send_signal(signal.SIGINT)

if __name__ == '__main__':
    q = Wrapper()
