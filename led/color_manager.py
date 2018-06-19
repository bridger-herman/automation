# REALLY HACKY FIX
# This fixes the symptom of Python deciding to reset instance variables when a
# multiprocessing Process ends.

from threading import Lock

COLOR_LOCK = Lock()

# TODO fix these rare deadlocks at some point
def update_col(c):
    #  print('waiting for file write lock')
    with COLOR_LOCK:
        with open('./color', 'w') as fout:
            #  print('updating color', c)
            fout.write(str(c))

def read_col():
    #  print('waiting for file read lock')
    with COLOR_LOCK:
        with open('./color', 'r') as fin:
            #  print('reading')
            return eval(fin.read())
