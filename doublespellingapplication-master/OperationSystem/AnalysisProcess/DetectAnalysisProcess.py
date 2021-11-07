from doubleSpellingApplication.OperationSystem.AnalysisProcess.BasicAnalysisProcess import BasicAnalysisProcess
import datetime
import numpy as np
import logging


class DetectAnalysisProcess(BasicAnalysisProcess):
    def __init__(self):
        self.operator_method = None
        self.current_end_point = None
        self.down_frequency_sample = None
        self.data_step = None
        self.threshold = None
        self.min_detection_window_layer = None
        self.continuous_detection_window_layer = None
        self.process_monitor_information = None
        self.base_threshold = None
        self.operation_state = None
        self.first_in = True

        self.logger = logging.getLogger("DoubleSpellingApplication.DetectAnalysisProcess")

    def initial(self, analysis_controller, schema_controller, experiment_information,real_time_reader,operation_state,operator_method, process_monitor_information):
        self.logger.debug("DetectAnalysisProcess.initial is called.")
        BasicAnalysisProcess.initial(self, experiment_information, real_time_reader)
        self.analysis_controller = analysis_controller
        self.schema_controller = schema_controller
        self.operation_state = operation_state

        self.operator_method = operator_method
        self.data_step = experiment_information.window_step_time * experiment_information.down_frequency_sample
        self.down_frequency_sample = experiment_information.down_frequency_sample
        self.base_threshold = experiment_information.threshold / 40

        self.min_detection_window_layer = experiment_information.min_detection_window_layer
        self.continuous_detection_window_layer = experiment_information.continuous_detection_window_layer

        self.current_end_point = []

        self.process_monitor_information = process_monitor_information

    def update(self,analysis_process_updata_obj):
        self.threshold = self.base_threshold * len(analysis_process_updata_obj.target_template_set)

    def run(self):
        data = self.real_time_reader.read_data()
        if data is None:
            return
        # if self.first_in:
        #     data = np.hstack((data, self.real_time_reader.read_data()))
        #     self.first_in = False
        # data = self.real_time_reader.pop_data()
        if self.analysis_controller.update_analysis_process.is_update_equalizer(data):
            self.analysis_controller.current_analysis_process = self.analysis_controller.update_analysis_process
            return

        # if len(self.current_end_point) == 0:
        #     start_point, trail_point = self.real_time_reader.get_stored_data_head_trail_point()
        #     self.current_end_point = trail_point
        #     return

        # data, start_point, end_point = self.real_time_reader.read_fixed_length_data(self.current_end_point, self.data_step)

        # tic = datetime.datetime.now()

        data = data[0:-1, :]

        # self.current_end_point = end_point
        # if np.mod(end_point, 10*self.data_step) <= self.data_step:
        #     print('当前计算数据点位置{0},当前时间{1}\n'.format(str(end_point), datetime.datetime.now()))
        # tic = datetime.datetime.now()
        self.operator_method.add_data(data)
        # toc = datetime.datetime.now()
        # print('add_data: ', toc-tic)
        tic = datetime.datetime.now()
        stop_flag, result, stop_window_index = self.get_result()
        toc = datetime.datetime.now()
        calculate_time = toc - tic
        print(calculate_time)

        self.process_monitor_information.set_calculate_time(calculate_time)

        if stop_flag:

            self.logger.debug('满足终止条件，第{0}个数据窗共{1}秒数据作为判决窗，识别结果{2}，执行时间{3}\n'.format(str(stop_window_index), str(stop_window_index * self.data_step/self.down_frequency_sample), str(result), datetime.datetime.now()))
            self.operation_state.current_detect_state = None
            # print(result)
            self.schema_controller.report(result)

            analysis_updata_obj = self.schema_controller.get_analysis_update_obj()
            self.analysis_controller.update(analysis_updata_obj)
            self.operator_method.clear()
            # self.real_time_reader.clear()
            self.analysis_controller.current_analysis_process = self.analysis_controller.wait_analysis_process
            return

    # def run(self):#test
    #     result = input()
    #     self.schema_controller.report(int(result))


    def clear(self):
        self.current_end_point = []
        self.operator_method.clear()
        self.real_time_reader.clear()

    def get_result(self):
        # tic = datetime.datetime.now()
        log_sum_probability = self.operator_method.get_stop_values()
        # toc = datetime.datetime.now()
        # print('get_stop_values',toc - tic)
        # tic = datetime.datetime.now()
        result_vector = self.operator_method.classify()
        # toc = datetime.datetime.now()
        # print('classify',toc - tic)
        windows_flag = []
        for i in range(0, len(log_sum_probability)):
            windows_flag.append(False)

        for i in range(self.min_detection_window_layer - 1, len(log_sum_probability)):
            last_result_vector = result_vector[i - self.continuous_detection_window_layer : i]

            windows_flag[i] = (log_sum_probability[i] < -np.log(1- self.threshold)) and not np.any(np.diff(last_result_vector))

        stop_flag = np.any(windows_flag)
        windows_flag = np.array(windows_flag)
        stop_window_index = np.argwhere(windows_flag == True)  # [0, 0]
        if stop_flag:
            stop_window_index = stop_window_index[0, 0]
        result = result_vector[stop_window_index]
        return stop_flag, result, stop_window_index



