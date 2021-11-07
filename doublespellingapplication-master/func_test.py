import numpy as np
import numba as nb
import sys

class A:
    def __init__(self):
        self.t = None
        self.a = np.random.rand(1000000)


if __name__ == '__main__':
    while True:
        c1 = A()
        c2 = A()

        t1=c1
        t2=c2

        c1.t = c2
        c2.t = c1

        c1.t=None
        c2.t=None

        # del c1
        # del c2

        print(sys.getrefcount(t1)-1)
        print(sys.getrefcount(t2)-1)
        print('\n')
