import logging

class OperateExchangeMessageOperator:

    def __init__(self):
        self.logger = logging.getLogger("DoubleSpellingApplication.OperateExchangeMessageOperator")
        self.exchange_message_management = None
        self.real_time_reader = None
        self.operation_state = None
        self.schema_controller = None
        self.analysis_controller = None
        self.events = ['CTNS', #connectToNeuroScan
                       'DCNS', #disconnectToNeuroScan;
                       'STAR', #startReceivedData
                       'STOP', #stopReceivedData
                       'CLRT', #ClearResultOperation
                       'STON', #StartOperation
                       'SPON', #StopOperation
                       'CSAL', #CloseAllOperation
                       'STRD', #StartRealTimeDetection
                       'EXIT'] #Exit Program

    def do_CTNS(self, event):
        self.logger.debug("received CTNS.")
        self.operation_state.receiver_state = 'CTNS'
        message = 'CTOK'
        self.exchange_message_management.send_exchange_message(message)
        self.logger.debug('成功连接到Neuracle服务器')
        #print('发送消息{}\n'.format(message.chId))

    def do_DCNS(self, event):
        self.logger.debug("received DCNS.")
        self.real_time_reader.disconnect()
        self.operation_state.receiver_state = 'DCNS'
        #message = ToStimulationSendingExchangeMessage.DisconnectToNeuroScanOK
        self.logger.debug('中断到Neuracle服务器连接')
        #self.exchange_message_management.sendExchangeMessage(message)
        #print('发送消息{}\n'.format(message.chId))
    def do_STAR(self, event):
        self.logger.debug("received STAR.")
        # self.real_time_reader.start_receive_data()
        self.operation_state.receiver_state = 'STAR'
        message = 'TROK'
        self.exchange_message_management.send_exchange_message(message)
        self.logger.debug('开始从NeuroScan服务器接收数据')
        #print('发送消息{}\n'.format(message.chId))

    def do_STOP(self, event):
        self.logger.debug("received STOP.")
        self.real_time_reader.stop_receive_data()
        #message = ToStimulationSendingExchangeMessage.StopReceiveOK
        self.operation_state.receiver_state = 'STOP'
        self.logger.debug('停止从NeuroScan服务器接收数据')
        #self.exchange_message_management.sendExchangeMessage(message)
        #print('发送消息{}\n'.format(message.chId))

    def do_STON(self, event):
        self.logger.debug("received STON.")
        self.operation_state.control_state = 'STON'
        self.logger.debug('设置为开始数据处理状态')
        # message = 'TNOK'
        # self.exchange_message_management.send_exchange_message(message)
        #print('发送消息{}\n'.format(message.chId))

    def do_SPON(self, event):
        self.logger.debug("received SPON.")
        #message = ToStimulationSendingExchangeMessage.StopOperationOK
        self.operation_state.control_state = 'SPON'
        self.logger.debug('设置为停止数据处理状态')
        #self.exchange_message_management.sendExchangeMessage(message)
        #print('发送消息{}\n'.format(message.chId))

    def do_CSAL(self, event):
        self.logger.debug("received CSAL.")
        #message = ToStimulationSendingExchangeMessage.CloseAllOperationOK
        self.operation_state.control_state = 'CSAL'
        self.logger.debug('设置为停止所有操作状态')
        #self.exchange_message_management.sendExchangeMessage(message)
        #print('发送消息{}\n'.format(message.chId))

    def do_CLRT(self, event):
        self.logger.debug("received CLRT.")
        self.schema_controller.clear()
        self.logger.debug('接收Del指令，已清理缓存内容')

    def do_EXIT(self, event):
        self.logger.debug("received EXIT.")
        self.operation_state.control_state = 'EXIT'
        self.logger.debug('处理程序准备退出')

    def do_STRD(self, event):
        self.logger.debug("received STRD.")
        self.operation_state.current_detect_state = 'STRD'
        self.logger.debug('准备进入实时处理模式')

    def add_listener(self, event_manager):
        event_manager.AddEventListener('CTNS', self.do_CTNS)
        event_manager.AddEventListener('DCNS', self.do_DCNS)
        event_manager.AddEventListener('STAR', self.do_STAR)
        event_manager.AddEventListener('STOP', self.do_STOP)
        event_manager.AddEventListener('CLRT', self.do_CLRT)
        event_manager.AddEventListener('STON', self.do_STON)
        event_manager.AddEventListener('SPON', self.do_SPON)
        event_manager.AddEventListener('CSAL', self.do_CSAL)
        event_manager.AddEventListener('STRD', self.do_STRD)
        event_manager.AddEventListener('EXIT', self.do_EXIT)

    def remove_listener(self, event_manager):
        event_manager.RemoveEventListener('CTNS', self.do_CTNS)
        event_manager.RemoveEventListener('DCNS', self.do_DCNS)
        event_manager.RemoveEventListener('STAR', self.do_STAR)
        event_manager.RemoveEventListener('STOP', self.do_STOP)
        event_manager.RemoveEventListener('CLRT', self.do_CLRT)
        event_manager.RemoveEventListener('STON', self.do_STON)
        event_manager.RemoveEventListener('SPON', self.do_SPON)
        event_manager.RemoveEventListener('CSAL', self.do_CSAL)
        event_manager.RemoveEventListener('STRD', self.do_STRD)
        event_manager.RemoveEventListener('EXIT', self.do_EXIT)