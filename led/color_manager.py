# REALLY HACKY FIX
# This fixes the symptom of Python deciding to reset instance variables when a
# multiprocessing Process ends.

from threading import Lock
from PIL import Image
import numpy as np

# Also using this to save the current color for use in brightness slider
# Interpolate from black -> c
def fade_colors(end_color):
        start_color = [0, 0, 0]

        width = 1024
        height = 50

        num_colors = len(start_color)
        color_diff = [(end_color[i] - start_color[i]) \
                for i in range(num_colors)]
        color_step = [d/width for d in color_diff]
        fading_colors = [[[int(start_color[i] + c*color_step[i] + 0.5) \
                for i in range(num_colors)] for c in range(width)] for r in range(height)]

        return Image.fromarray(np.asarray(fading_colors, dtype=np.uint8), mode='RGB')

COLOR_LOCK = Lock()

# TODO fix these rare deadlocks at some point
def update_col(c):
    with COLOR_LOCK:
        with open('./color', 'w') as fout:
            fout.write(str(c))
            fade_colors(c).save('./brightness_slider.png')

def read_col():
    with COLOR_LOCK:
        with open('./color', 'r') as fin:
            return eval(fin.read())
