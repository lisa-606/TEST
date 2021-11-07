from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.EventManager import EventManager
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.CommonModule.ResultTransferModel import ResultTransferModel
import datetime
import logging

class StimulationExchangeMessageOperator:
    def __init__(self):
        #self.event_manager = EventManager()
        self.experiment_information = None
        self.state_monitor = None
        self.controller = None

        self.events = ['CTOK',
                       'DCOK',
                       'TROK',
                       'PROK',
                       'TNOK',
                       'PNOK',
                       'CAOK',
                       'STSN',
                       'RSLT']
        self.logger = logging.getLogger("DoubleSpellingApplication.StimulationExchangeMessageOperator")

    def do_CTOK(self,event):
        self.state_monitor.status = 'CTOK'
        message = event.message
        self.logger.debug('接收消息{0}，设置监视器状态{1}\n'.format('CTOK', self.state_monitor.status))

    def do_DCOK(self, event):
        self.state_monitor.status = 'DCOK'
        message = event.message
        self.logger.debug('接收消息{0}，设置监视器状态{1}\n'.format('DCOK', self.state_monitor.status))

    def do_TROK(self, event):
        self.state_monitor.status = 'TROK'
        message = event.message
        self.logger.debug('接收消息{0}，设置监视器状态{1}\n'.format('TROK', self.state_monitor.status))

    def do_PROK(self, event):
        self.state_monitor.status = 'PROK'
        message = event.message
        self.logger.debug('接收消息{0}，设置监视器状态{1}\n'.format('PROK', self.state_monitor.status))

    def do_TNOK(self, event):
        self.state_monitor.status = 'TNOK'
        message = event.message
        self.logger.debug('接收消息{0}，设置监视器状态{1}\n'.format('TNOK', self.state_monitor.status))

    def do_PNOK(self, event):
        self.state_monitor.status = 'PNOK'
        message = event.message
        self.logger.debug('接收消息{0}，设置监视器状态{1}\n'.format('PNOK', self.state_monitor.status))


    def do_CAOK(self, event):
        self.state_monitor.status = 'CAOK'
        message = event.message
        self.logger.debug('接收消息{0}，设置监视器状态{1}\n'.format('CAOK', self.state_monitor.status))

    def do_STSN(self, event):
        self.state_monitor.status = 'STSN'
        message = event.message
        self.logger.debug('接收消息{0}，设置监视器状态{1}\n'.format('STSN', self.state_monitor.status))

    def do_RSLT(self, event):
        message = event.message

        #result_transfer_model = ResultTransferModelConvertor.to_transfer_model(message_body)
        result_transfer_model = ResultTransferModel()
        result_transfer_model.prepare_last_time=0
        result_transfer_model.finish_last_time=0
        result_transfer_model.alphabet_id = message['result']
        result_transfer_model.next_mode = message['next_mode']
        result_transfer_model.up_text = message['up_text']
        result_transfer_model.down_text = message['down_text']
        result_transfer_model.candidate_char = message['candidate_char']
        result_transfer_model.speak = message['speak']

        self.logger.debug('收到返回结果{}：'.format(datetime.datetime.now()))
        self.logger.debug(result_transfer_model)

        self.controller.change(result_transfer_model)

    def add_listener(self, event_manager):
        event_manager.AddEventListener('CTOK', self.do_CTOK)
        event_manager.AddEventListener('DCOK', self.do_DCOK)
        event_manager.AddEventListener('TROK', self.do_TROK)
        event_manager.AddEventListener('PROK', self.do_PROK)
        event_manager.AddEventListener('TNOK', self.do_TNOK)
        event_manager.AddEventListener('PNOK', self.do_PNOK)
        event_manager.AddEventListener('CAOK', self.do_CAOK)
        event_manager.AddEventListener('STSN', self.do_STSN)
        event_manager.AddEventListener('RSLT', self.do_RSLT)

    def remove_listener(self, event_manager):
        event_manager.RemoveEventListener('CTOK', self.do_CTOK)
        event_manager.RemoveEventListener('DCOK', self.do_DCOK)
        event_manager.RemoveEventListener('TROK', self.do_TROK)
        event_manager.RemoveEventListener('PROK', self.do_PROK)
        event_manager.RemoveEventListener('TNOK', self.do_TNOK)
        event_manager.RemoveEventListener('PNOK', self.do_PNOK)
        event_manager.RemoveEventListener('CAOK', self.do_CAOK)
        event_manager.RemoveEventListener('STSN', self.do_STSN)
        event_manager.RemoveEventListener('RSLT', self.do_RSLT)