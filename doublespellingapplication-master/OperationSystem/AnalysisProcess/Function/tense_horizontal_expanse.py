import numpy as np


def tense_horizontal_expanse(x):
    n = x.shape
    y = x.reshape(n[0], n[1] * n[2], order='F')
    return np.mat(y)
