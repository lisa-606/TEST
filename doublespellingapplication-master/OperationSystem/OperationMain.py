import datetime
import time
import sys
sys.path.append('..')


from doubleSpellingApplication.OperationSystem.OperationState.OperationState import OperationState
from doubleSpellingApplication.OperationSystem.OperateExchangeMessageOperator import OperateExchangeMessageOperator
from doubleSpellingApplication.OperationSystem.Singleton.SingletonProcessMonitorInformation import singleton_process_monitor_information
from doubleSpellingApplication.CommonSystem.MessageReceiver.ExchangeMessageManagement import ExchangeMessageManagement
from doubleSpellingApplication.CommonSystem.ExperimentInformation.create_experiment_information import create_experiment_information
from doubleSpellingApplication.OperationSystem.Singleton.SingletonSchemaController import singleton_schema_controller
from doubleSpellingApplication.OperationSystem.Singleton.SingletonAnalysisController import singleton_analysis_controller
from doubleSpellingApplication.OperationSystem.ReceiveDataClient.FakeDataReader import FakeDataReader
from doubleSpellingApplication.OperationSystem.ReceiveDataClient.RealTimeReader import  RealTimeReader


# 启动控制接收及结果管理器
operation_state = OperationState()  # 流程状态定义（数据采集状态、基本控制状态、检测阶段处理状态）

operate_exchange_message_operator = OperateExchangeMessageOperator()  # 处理端接收消息处理函数

operate_exchange_message_operator.operation_state = operation_state

# 初始化处理信息记录
process_monitor_information = singleton_process_monitor_information

process_monitor_information.reset()

# 交换信息中心管理器
topic_ope_receive = 'stim_to_ope'
topic_ope_send = 'ope_to_stim'
exchange_message_management = ExchangeMessageManagement(operate_exchange_message_operator, topic_receive = topic_ope_receive, topic_send=topic_ope_send)

# 创建实验信息从脚本函数中生成
experiment_information = create_experiment_information('[]', '[]')

# 放大器设置
real_time_reader = FakeDataReader()
# real_time_reader = RealTimeReader()

operate_exchange_message_operator.exchange_message_management = exchange_message_management
operate_exchange_message_operator.real_time_reader = real_time_reader
operate_exchange_message_operator.schema_controller = singleton_schema_controller
operate_exchange_message_operator.analysis_controller = singleton_analysis_controller

# 生成检测模式识别策略控制器
schema_controller = singleton_schema_controller
schema_controller.initial(experiment_information, exchange_message_management)

# 生成脑电信号分析检测控制器
analysis_controller = singleton_analysis_controller
analysis_controller.initial(schema_controller, experiment_information, real_time_reader, operation_state)

analysis_updata_obj = schema_controller.get_analysis_update_obj()
analysis_controller.update(analysis_updata_obj)

# 启动与刺激系统数据交换器
exchange_message_management.start()

print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(operation_state.control_state,
            'STON', datetime.datetime.now()))
while operation_state.control_state != 'STON':
    # 等待开始处理标识
    time.sleep(0.5)

real_time_reader.connect()

while operation_state.control_state != 'EXIT':
    analysis_controller.run()
    # time.sleep(0.1)

# real_time_reader.stop_receive_data()
message = 'PROK'
exchange_message_management.send_exchange_message(message)
operation_state.receiver_state = 'STOP'
print('停止从NeuroScan服务器接收数据')

real_time_reader.disconnect()
operation_state.receiver_state = 'DCNS'
print('中断到NeuroScan服务器连接')
message = 'DCOK'
exchange_message_management.send_exchange_message(message)

print('处理系统关闭,{0}\n'.format(datetime.datetime.now()))
exchange_message_management.stop()
exchange_message_management.delete()
print('连接结束,{0}\n', datetime.datetime.now())
print('中断到无人机连接器连接')
message = 'CAOK'
exchange_message_management.send_exchange_message(message)
