import scipy.io as scio
from doubleSpellingApplication.OperationSystem.ReceiveDataClient.RealTimeReaderInterface import RealTimeReaderInterface
from doubleSpellingApplication.OperationSystem.ReceiveDataClient.DataCash import DataCash
import datetime
import time
from scipy import signal
from doubleSpellingApplication.CommonSystem.ExperimentInformation.PreprocessFilter import PreprocessFilter
from doubleSpellingApplication.OperationSystem.AnalysisProcess.Function.signaltools import lfilter
import numpy as np

import logging


class RealTimeReader(RealTimeReaderInterface):
    def __init__(self):
        self.topic = 'NeuracleEEG_sy'
        self.data_cashe = DataCash('NeuracleEEG', self.topic)
        self.stop_flag = False

        self.notch = PreprocessFilter()
        self.notch.B = np.array([0.957020174408697, 0, 0, 0, 0, -0.957020174408697])
        self.notch.A = np.array([1, 0, 0, 0, 0, -0.914040348817395])
        self.Zi = None

        self.logger = logging.getLogger("DoubleSpellingApplication.RealTimeReader")


    def get_message_queue_size(self):
        # return 10001
        return self.data_cashe.getMessageQueueSize()

    def read_data(self):
        # self.logger.debug('data_cashe.getMessageQueueSize(): ' + str(self.get_message_queue_size()))
        concate_data = np.zeros((10, 0))
        while concate_data.shape[1] != 120:
            data = self.data_cashe.readData(0, 1)
            while data is None:
                if self.stop_flag == True:
                    return data
                data = self.data_cashe.readData(0, 1)

            concate_data = np.hstack((concate_data, data[0]))
        data = concate_data[0:-1, ::4]
            # time.sleep(0.1)
        self.logger.debug('read_data: ' + str(datetime.datetime.now()) + 'MessageQueueSize: ' + str(self.data_cashe.getMessageQueueSize()))

        data_before_filter = data

        data_after_filter = self.notch_filter(data_before_filter, self.Zi)


        return data_after_filter
        # return data[0]

    def read_new_data(self, point_count):
       return self.data_cashe.readNewData(point_count)

    def read_fixed_length_data(self, start_point, length):
        return self.data_cashe.readFixedData(start_point, length)

    def connect(self):
        self.logger.debug("RealtimeReader.connect is called.")
        self.data_cashe.start()

    def disconnect(self):
        self.logger.debug("RealtimeReader.disconnect is called.")
        self.data_cashe.stop_flag = True
        self.stop_flag = True
        # self.data_cashe.join()

    def clear(self):
        self.data_cashe.clear()

    def pop_data(self):
        data = self.data_cashe.messageQueue.pop()
        while data is None:
            data = self.data_cashe.messageQueue.pop()
            # time.sleep(0.1)
        print('data.shape: ',data.shape)
        return data
        # return self.data_cashe.messageQueue.pop()

    # def notch_filter(self, data, Zi=None):
    #     Zf = np.array(np.zeros((data.shape[0], 2)))  # , dtype=complex
    #     output_data = np.array(np.zeros((data.shape), dtype=complex))
    #     for i in range(0, data.shape[0]):
    #         if self.Zi is not None:
    #
    #             temp_data, Zf_temp = signal.lfilter(self.notch.B, self.notch.A, data[i, :],
    #                                                 zi=Zi[i, :])
    #         else:
    #             Zf_temp1 = signal.lfilter_zi(self.notch.B, self.notch.A)
    #
    #             t, Zf_temp = signal.lfilter(self.notch.B, self.notch.A,
    #                                         data[i, :], zi=Zf_temp1)  # zi= np.ones((filter_cell_matrix.shape[2]-1,))
    #             # Zf_temp = signal.lfiltic(filter_cell_matrix[i, j, :], np.array([1]), t)
    #
    #             temp_data = t
    #
    #         Zf[i, :] = Zf_temp
    #
    #         # output_data[i,:] = sum(cat(1, tempData{i,:}), 1).'
    #         output_data[i, :] = temp_data
    #     self.Zi = Zf
    #     return output_data

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