import numpy as np


class ProcessMonitorInformation:
    def __init__(self):
        self.calculate_time = np.empty((1,1000000))
        self.i = 1

    def reset(self):
        self.calculate_time = np.empty((1,1000000),dtype=object)
        self.i = 1

    def set_calculate_time(self, calculate_time):
        self.calculate_time[:, self.i] = calculate_time
        self.i = (self.i % self.calculate_time.shape[1]) +1
