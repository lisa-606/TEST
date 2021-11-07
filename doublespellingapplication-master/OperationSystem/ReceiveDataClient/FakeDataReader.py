import scipy.io as scio
from doubleSpellingApplication.OperationSystem.ReceiveDataClient.RealTimeReaderInterface import RealTimeReaderInterface
import datetime
from scipy import signal
from doubleSpellingApplication.CommonSystem.ExperimentInformation.PreprocessFilter import PreprocessFilter
from doubleSpellingApplication.OperationSystem.AnalysisProcess.Function.signaltools import lfilter
import numpy as np
import os

class FakeDataReader(RealTimeReaderInterface):
    def __init__(self):
        data_file = os.path.join(os.path.dirname(__file__), r"fakeData.mat")
        data = scio.loadmat(data_file)
        self.fake_data = data['outData']
        self.data_step = 30
        self.pointer = 0

        self.notch = PreprocessFilter()
        self.notch.B=np.array([0.957020174408697, 0, 0, 0, 0, -0.957020174408697])
        self.notch.A = np.array([1, 0, 0, 0, 0, -0.914040348817395])
        self.Zi = None

    def get_message_queue_size(self):
        return self.fake_data.shape[1]

    def read_data(self): #  , start_point, end_point
        out = self.fake_data[:, self.pointer : self.pointer+self.data_step]
        self.pointer = self.pointer + self.data_step
        print('read data!!!!!  ', datetime.datetime.now(), '  pointer: ', self.pointer)
        if self.pointer > self.fake_data.shape[1]:
            raise Exception('没数据啦')


        data_after_filter = self.notch_filter(out, self.Zi)

        return data_after_filter
        # return out

    def read_new_data(self, point_count):
        pass  # 1从尾巴取

    def read_fixed_length_data(self, start_point, length):
        pass  # 1从起点取一定长度

    def clear(self):
        pass

    def notch_filter(self, data, Zi=None):
        Zf = np.array(np.zeros((data.shape[0], 5)))  # , dtype=complex
        output_data = np.array(np.zeros((data.shape)))
        for i in range(0, data.shape[0]):
            if self.Zi is not None:

                temp_data, Zf_temp = signal.lfilter(self.notch.B, self.notch.A, data[i, :],
                                                    zi=Zi[i, :])
                # temp_data = signal.lfilter(self.notch.B, self.notch.A, data[i, :])
            else:
                Zf_temp1 = signal.lfilter_zi(self.notch.B, self.notch.A)

                t, Zf_temp = signal.lfilter(self.notch.B, self.notch.A,
                                     data[i, :], zi=Zf_temp1)  # zi= np.ones((filter_cell_matrix.shape[2]-1,))
                # Zf_temp = signal.lfiltic(filter_cell_matrix[i, j, :], np.array([1]), t)

                temp_data = t
                # temp_data = signal.lfilter(self.notch.B, self.notch.A, data[i, :])

            Zf[i, :] = Zf_temp

            # output_data[i,:] = sum(cat(1, tempData{i,:}), 1).'
            output_data[i, :] = temp_data


        self.Zi = Zf
        return output_data
        # if Zi is not None:
        #     temp_data, Zf_temp = signal.lfilter(self.notch.B, self.notch.A, data, zi=Zi)
        # else:
        #     Zf_temp1 = signal.lfilter_zi(self.notch.B, self.notch.A)
        #
        #     temp_data, Zf_temp = signal.lfilter(self.notch.B, self.notch.A,data, zi=Zf_temp1)
        #
        # self.Zi = Zf_temp
        # return temp_data
