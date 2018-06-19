# REALLY HACKY FIX
# This fixes the symptom of Python deciding to reset instance variables when a
# multiprocessing Process ends.

from threading import Lock

COLOR_LOCK = Lock()

def update_col(c):
    with COLOR_LOCK:
        with open('./color', 'w') as fout:
            print('updating color', c)
            fout.write(str(c))

def read_col():
    with COLOR_LOCK:
        with open('./color', 'r') as fin:
            return eval(fin.read())
