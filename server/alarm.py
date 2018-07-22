import time
from threading import Thread
from datetime import datetime, timedelta

class Alarm:
    def __init__(self, alarm_time, callback, args=()):
        self.alarm_time = alarm_time
        self.callback = callback
        self.args = args
        self.thread = Thread(target=self.wait_for_time)
        self.thread.start()

    def wait_for_time(self):
        waiting = True
        while waiting:
            current_time = datetime.now()
            if self.alarm_time - current_time < timedelta(seconds=1):
                waiting = False
            time.sleep(0.5)
        self.callback(*self.args)
