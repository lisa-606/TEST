from doubleSpellingApplication.OperationSystem.SchemaProcess.BasicSchemaProcess import BasicSchemaProcess
from doubleSpellingApplication.OperationSystem.AnalysisProcess.ValueObj.AnalysisProcessUpdataObj import AnalysisProcessUpdataObj
import datetime
import numpy as np
import socket
import time


class UAVControlInputSchemaProcess(BasicSchemaProcess):
    def __init__(self):
        super(BasicSchemaProcess, self).__init__()

        self.model_index = None

        #模式信息
        self.schema_process_information = None

        #字母表
        #{'ID', 'UAVCOMMANDID', 'DISPLAYCHAR', 'FREQUENCY', 'PHASE'}
        self.target_table = None

        #数据写入模块
        self.writter = None

        #实验信息
        self.experiment_information = None

        self.target_template_set = None

        self.uav_connector = None

        #准备阶段时间
        self.prepare_last_time = None

        #休息时间
        self.finish_last_time = None

    def initial(self, experiment_information):
        #初始化控制器
        BasicSchemaProcess.initial(self)

        #初始化基准参数
        self.model_index = 1

        self.experiment_information = experiment_information

        self.schema_process_information = experiment_information.schema_process_information

        self.target_table = self.schema_process_information.target_table

        #准备阶段时间
        self.prepare_last_time = experiment_information.prepare_last_time

        #休息时间
        self.finish_last_time = experiment_information.finish_last_time

        #候选字符

        self.target_template_set = self.create_target_template_set(self.target_table)

        #???self.uav_connector = UAVConnectorDJIMavic2Implement.uavConnector

        # self.socket_test = socket.socket()
        # self.socket_test.connect(('10.28.230.43', 12306))
        # print("已连接")


    def get_analysis_updata_obj(self):
        analysis_process_updata_obj = AnalysisProcessUpdataObj()
        analysis_process_updata_obj.target_template_set = self.target_template_set
        return analysis_process_updata_obj

    def clear(self):
        pass

    def prepare(self):
        pass

    def over(self):
        pass

    def report(self, result_index):

        result_id = result_index
        #识别结果
        print('\n{0}.report:本次识别结果{1}，刺激频率{2}，执行时间{3}\n'.format(self.__class__.__name__, self.target_table['DISPLAYCHAR'][result_id], self.target_table['FREQUENCY'][result_id], datetime.datetime.now()))

        result_obj = self.recongize(result_id)

        '''
        uavCommands = enumeration('UAVCommand');
        uavCommand = uavCommands([uavCommands.id] == resultId);
        self.uavConnector.sendUAVCommand(uavCommand);
        '''
        uav_test_list = ["UVDW", "UVUP", "UVTL", "UVTR", "UVFB", "UVFF", "UVFL", "UVFR", "UVLD", "UVTO"]  # , "UVTO", "UVLD"]


        # self.socket_test.send(bytes(uav_test_list[result_id], encoding="utf-8"))
        # print("发送成功！结果："+uav_test_list[result_id])

        time.sleep(0.5)
        return result_obj

    def recongize(self, result_id):
        #总体识别函数, sendStruct中需要包括
        #perpareLastTime, finishLastTime, alphabetId, nextModelIndex, resultString, candidateSet

        #补充其他参数
        result_obj = {'prepare_last_time' : self.prepare_last_time,
                      'finish_last_time' : self.finish_last_time,
                      'alphabet_id' : result_id}
        return result_obj

    def create_target_template_set(self, frequency_phase_table):
    # 初始化模板
        frequency_set = frequency_phase_table['FREQUENCY']

        #模板容量足够大
        sample_count = (self.experiment_information.max_window_time + self.experiment_information.offset_time + 1) * self.experiment_information.down_frequency_sample
        target_template_set = []
        for i in range(len(frequency_set) - 1, -1, -1):
            test_fres = np.mat((frequency_set[i] * (np.arange(1, self.experiment_information.multiplicate_time + 1, 1))).reshape(self.experiment_information.multiplicate_time, 1, order = 'F'))
            t = np.mat(np.arange(0, 1 / self.experiment_information.down_frequency_sample * (sample_count), 1 / self.experiment_information.down_frequency_sample))
            target_template_set.insert(0, np.vstack((np.exp(-1j * 2 * np.pi * test_fres * t), np.exp(1j * 2 * np.pi * test_fres * t))))
        return target_template_set
