import datetime
import time
import threading
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
# print("double spelling add before: {}".format(sys.path))
# sys.path.append(os.path.join(os.path.dirname(os.getcwd()), 'doubleSpellingApplication'))
# print("double spelling add after: {}".format(sys.path))
from doubleSpellingApplication.OperationSystem.OperationState.OperationState import OperationState
from doubleSpellingApplication.OperationSystem.OperateExchangeMessageOperator import OperateExchangeMessageOperator
from doubleSpellingApplication.CommonSystem.MessageReceiver.ExchangeMessageManagement import ExchangeMessageManagement
from doubleSpellingApplication.CommonSystem.ExperimentInformation.create_experiment_information import create_experiment_information
from doubleSpellingApplication.OperationSystem.ReceiveDataClient.RealTimeReader import  RealTimeReader
from doubleSpellingApplication.OperationSystem.ReceiveDataClient.FakeDataReader import FakeDataReader
from doubleSpellingApplication.OperationSystem.ProcessMonitorInformation.ProcessMonitorInformation import ProcessMonitorInformation
from doubleSpellingApplication.OperationSystem.SchemaProcess.SchemaController import SchemaController
from doubleSpellingApplication.OperationSystem.AnalysisProcess.AnalysisController import AnalysisController
# from doubleSpellingApplication.OperationSystem.subsystemLCInterface import SubsystemLCInterface
from interfaces.subsystemLCInterface import SubsystemLCInterface


class DoubleSpellingOpeController(SubsystemLCInterface):
    def __init__(self):
        self.operation_state = None
        self.operate_exchange_message_operator = None
        self.process_monitor_information = None
        self.exchange_message_management = None
        self.experiment_information = None
        self.real_time_reader = None
        self.schema_controller = None
        self.analysis_controller = None
        self.stop_flag = False

        self.logger = logging.getLogger('DoubleSpellingApplication')
        self.logger.setLevel(logging.DEBUG)
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        father_path = os.path.join(os.path.dirname(__file__), os.path.pardir)
        log_file_handler = TimedRotatingFileHandler(filename=fr'{father_path}/dslogs/DoubleSpellingApplication', when="D", interval=1,
                                                    backupCount=30, encoding='utf-8')

        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        log_file_handler.setFormatter(formatter)
        self.logger.addHandler(log_file_handler)

    def initial(self, keyList = None, keyPressedCallback = None,  config = None):
        self.logger.debug("wjsDoubleSpellingOpeController.initial in subsystem instance is called")
        try:
            self.operation_state = OperationState()  # 流程状态定义（数据采集状态、基本控制状态、检测阶段处理状态）

            self.operate_exchange_message_operator = OperateExchangeMessageOperator()  # 处理端接收消息处理函数

            self.operate_exchange_message_operator.operation_state = self.operation_state

            # 初始化处理信息记录
            self.process_monitor_information = ProcessMonitorInformation()

            self.process_monitor_information.reset()

            # 交换信息中心管理器
            topic_ope_receive = 'stim_to_ope_suyan'
            topic_ope_send = 'ope_to_stim_suyan'
            self.exchange_message_management = ExchangeMessageManagement(self.operate_exchange_message_operator,
                                                                    topic_receive=topic_ope_receive,
                                                                    topic_send=topic_ope_send)

            # 创建实验信息从脚本函数中生成
            self.experiment_information = create_experiment_information('[]', '[]')

            # 放大器设置
            self.real_time_reader = FakeDataReader()
            # self.real_time_reader = RealTimeReader()
            self.real_time_reader.connect()

            # 生成检测模式识别策略控制器
            self.schema_controller = SchemaController()
            self.schema_controller.initial(self.experiment_information, self.exchange_message_management)

            # 生成脑电信号分析检测控制器
            self.analysis_controller = AnalysisController()
            self.analysis_controller.initial(self.schema_controller, self.experiment_information, self.real_time_reader,
                                             self.operation_state, self.process_monitor_information)

            self.operate_exchange_message_operator.exchange_message_management = self.exchange_message_management
            self.operate_exchange_message_operator.real_time_reader = self.real_time_reader
            self.operate_exchange_message_operator.schema_controller = self.schema_controller
            self.operate_exchange_message_operator.analysis_controller = self.analysis_controller


            analysis_updata_obj = self.schema_controller.get_analysis_update_obj()
            self.analysis_controller.update(analysis_updata_obj)

            # 启动与刺激系统数据交换器
            self.exchange_message_management.start()
            self.logger.debug('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(self.operation_state.control_state,
                                                          'STON', datetime.datetime.now()))
        except Exception as e:
            self.logger.fatal(e, exc_info=True)
            self.stop()
            raise e

    def start(self):
        self.logger.debug("DoubleSpellingOpeController.start is called.")
        try:

            while self.operation_state.control_state != 'STON':
                if(self.stop_flag == True):
                    break
                # 等待开始处理标识
                time.sleep(0.5)

            # self.real_time_reader.connect()

            while self.real_time_reader.get_message_queue_size() <= 800:
                if (self.stop_flag == True):
                    break
                continue

            message = 'TNOK'
            self.exchange_message_management.send_exchange_message(message)

            self.analysis_controller.current_analysis_process = self.analysis_controller.detect_analysis_process
            # self.analysis_controller.current_analysis_process = self.analysis_controller.wait_analysis_process

            while self.operation_state.control_state != 'EXIT':
                self.analysis_controller.run()
                # time.sleep(0.1)

            # real_time_reader.stop_receive_data()
            # message = 'PROK'
            # self.exchange_message_management.send_exchange_message(message)
            # self.operation_state.receiver_state = 'STOP'
            # print('停止从NeuroScan服务器接收数据')
            #
            # self.real_time_reader.disconnect()
            # self.operation_state.receiver_state = 'DCNS'
            # print('中断到NeuroScan服务器连接')
            # message = 'DCOK'
            # self.exchange_message_management.send_exchange_message(message)
            #
            # print('处理系统关闭,{0}\n'.format(datetime.datetime.now()))
            # self.exchange_message_management.stop()
            # self.exchange_message_management.delete()
            # print('连接结束,{0}\n', datetime.datetime.now())
            # print('中断到无人机连接器连接')
            # message = 'CAOK'
            # self.exchange_message_management.send_exchange_message(message)
            self.logger.debug("DoubleSpellingOpeController.start is returned.")

        except Exception as e:
            self.logger.fatal(e, exc_info=True)
            self.stop()
            raise e

    def stop(self):
        self.logger.debug("DoubleSpellingOpeController.stop is called.")
        # time.sleep(40)
        self.operation_state.control_state = 'EXIT'
        self.real_time_reader.disconnect()
        self.exchange_message_management.stop()
        self.stop_flag = True
        self.logger.debug("DoubleSpellingOpeController.stop is returned.")

        # print("double spelling remove before: {}".format(sys.path))
        # sys.path.remove(os.path.join(os.path.dirname(os.getcwd()), 'doubleSpellingApplication'))
        # print("double spelling remove after: {}".format(sys.path))
        # print(str(threading.enumerate()))

if __name__ == '__main__':
    controller = DoubleSpellingOpeController()
    # stop_thread = Thread(name = 'stop_thread',target = controller.stop,)

    controller.initial()
    time.sleep(5)

    # stop_thread.start()

    print(str(threading.enumerate()))

    controller.start()

