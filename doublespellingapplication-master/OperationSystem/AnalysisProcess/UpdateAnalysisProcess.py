from doubleSpellingApplication.OperationSystem.AnalysisProcess.BasicAnalysisProcess import BasicAnalysisProcess
from doubleSpellingApplication.OperationSystem.AnalysisProcess.Function.EstimateSTEqualizer import EstimateSTEqualizer
import datetime
import numpy as np
import logging


class UpdateAnalysisProcess(BasicAnalysisProcess):
    def __init__(self):
        self.operator_method = None
        self.equalizer_estimate_data_length = None
        self.equalizer_order = None
        self.equalizer_update_point = None
        self.equalizer_update_data_length = None
        self.cashe_data = None

        self.logger = logging.getLogger("DoubleSpellingApplication.UpdateAnalysisProcess")

    def initial(self, analysis_controller, schema_controller, experiment_information, real_time_reader, operator_method):
        self.logger.debug("UpdateAnalysisProcess.initial is called.")
        BasicAnalysisProcess.initial(self, experiment_information, real_time_reader)
        self.analysis_controller = analysis_controller
        self.schema_controller = schema_controller
        self.operator_method = operator_method
        self.equalizer_update_data_length = experiment_information.equalizer_update_time * experiment_information.down_frequency_sample
        self.equalizer_estimate_data_length = experiment_information.equalizer_estimate_time * experiment_information.down_frequency_sample
        self.equalizer_order = experiment_information.equalizer_order
        self.equalizer_update_point = []
        self.down_frequency_sample = experiment_information.down_frequency_sample

    def update(self, analysis_process_updata_obj):
        pass

    def run(self):
        tic = datetime.datetime.now()
        data_length = self.cashe_data.shape[1]
        if data_length < self.equalizer_estimate_data_length:
            data = self.cashe_data
        #     [data, start_point, end_point] = self.real_time_reader.read_data()
        else:
            temp = self.cashe_data[:, self.cashe_data.shape[1]-self.equalizer_estimate_data_length+1:]
            data = np.hstack((temp, np.random.rand(9,30)))
            self.cashe_data = self.cashe_data[:, self.equalizer_update_data_length:-1]
        # data = self.cashe_data
        # 丢弃trigger导
        data = data[0:-1, :]

        # downSampleData = obj.downSampleFun(data, size(data, 2));

        equalizer, Pi = EstimateSTEqualizer(data, self.equalizer_order)

        self.operator_method.set_spatio_temporal_equalizer(equalizer)

        current_max_window_index = self.operator_method.current_max_window_index

        window_step = self.operator_method.window_step

        # 提取出最后currentMaxWindowIndex * windowStep数据
        cal_data = data[:, int(data.shape[1] - int(window_step * current_max_window_index)):]

        self.operator_method.clear()
        # self.real_time_reader.clear()

        # 重新计算各个窗内数据指标
        for i in range(0, current_max_window_index):
            self.operator_method.add_data(cal_data[:, int(i * window_step) : int((i+1) * window_step)])

        toc = datetime.datetime.now()
        update_time = toc - tic
        self.logger.debug('\n\n均衡器更新完成，所用数据长度{0}，更新所用计算时间{1}，当前时间{2}\n\n'.format(data.shape[1], update_time, datetime.datetime.now()))

        # self.equalizer_update_point = end_point

        # self.cashe_data = np.array(np.zeros((self.cashe_data.shape[0], 1)))
        # self.cashe_data = self.cashe_data[:,  self.equalizer_update_data_length:-1]
        # 进入检测模式
        self.analysis_controller.current_analysis_process = self.analysis_controller.detect_analysis_process

        # self.analysis_controller.current_analysis_process.current_end_point = end_point

    def is_update_equalizer(self, data):
        # 如果是第一次进入，则将截止点设为当前数据点
        if self.cashe_data is None:
            self.cashe_data = np.random.rand(9,30)#data
            while self.cashe_data.shape[1] < self.equalizer_estimate_data_length:
                self.cashe_data = np.hstack((self.cashe_data, self.real_time_reader.read_data()))

            # self.cashe_data = np.random.rand(9,30)
            flag = True
            return flag

        self.cashe_data = np.hstack((self.cashe_data, data))

        # trail_point = self.real_time_reader.get_stored_data_head_trail_point()

        if self.cashe_data.shape[1] < self.equalizer_estimate_data_length:
            # self.equalizer_update_point = trail_point
            # 为false表示刚启动时不更新，反之为启动时更新
            flag = False
        else:
            flag = True
        return flag
