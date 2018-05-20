import numpy as np

# clamp a color (represented as np.array)
def clamp(c):
    c = np.array(c)
    c[c > 255] = 255
    c[c < 0] = 0
    return c
