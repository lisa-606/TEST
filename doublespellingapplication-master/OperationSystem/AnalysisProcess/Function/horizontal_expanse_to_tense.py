import numpy as np


def horizontal_expanse_to_tense(x, order):
    n = x.shape
    if np.mod(n[1], order):
        print('error(维度不匹配)')
    t = x.A
    y = t.reshape(n[0], int(n[1] / order), int(order), order="F")
    return y