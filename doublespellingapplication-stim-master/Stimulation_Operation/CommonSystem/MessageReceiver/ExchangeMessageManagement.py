from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.EventManager import EventManager, Event
import queue
from threading import Thread
import uuid
import os
import logging
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.receive_exchange_message_fcn import receive_exchange_message_fcn
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.operate_exchange_message_fcn import operate_exchange_message_fcn
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.receive_exchange_message_fcn_local_test import receive_exchange_message_fcn_local_test
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.EEGPlatformCommunicationModule.implement.CommunicationConsumer import CommunicationConsumer
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.EEGPlatformCommunicationModule.implement.CommunicationProducer import CommunicationProducer
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.EEGPlatformCommunicationModule.implement.CommunicationInitial import CommunicationInitial


# consumer_config_path = r"..\CommonSystem\MessageReceiver\config\consumer-config.json"
# producer_config_path = r"..\CommonSystem\MessageReceiver\config\producer-config.json"

consumer_config_path = os.path.join(os.path.dirname(__file__), 'config', 'consumer-config.json')
producer_config_path = os.path.join(os.path.dirname(__file__), 'config', 'producer-config.json')
# father_path = os.path.dirname(__file__)
# consumer_config_path = os.path.join(os.path.join(father_path, r"config"), 'consumer-config.json')
# producer_config_path = os.path.join(os.path.join(father_path, r"config"), 'producer-config.json')

class ExchangeMessageManagement:
    def __init__(self, exchange_message_operator, topic_receive, topic_send):
        self.receive_exchange_message_thread = None
        self.operator_exchange_message_thread = None
        self.message_queue = None
        self.exchange_message_operator = exchange_message_operator
        self.topic_receive = topic_receive
        self.topic_send = topic_send
        topicCreateResult = CommunicationInitial.topicCreate(self.topic_send, producer_config_path)
        self.producer = CommunicationProducer(producer_config_path)
        self.consumer = CommunicationConsumer(consumer_config_path, str(uuid.uuid1()), self.topic_receive)
        #self.listener_handles = None
        self.event_manager = EventManager()
        self.logger = logging.getLogger("DoubleSpellingApplication.ExchangeMessageManagement")
        self.initial(exchange_message_operator)

        self.stop_flag = False

    def initial(self, exchange_message_operator):
        self.logger.debug("ExchangeMessageManagement.initial is called.")
        #self.event_manager = EventManager()
        self.exchange_message_operator = exchange_message_operator
        self.message_queue = queue.Queue(0)

        if self.event_manager.count != 0:
            self.remove_listener_from_operator()

        self.add_listener_from_operator()

        self.receive_exchange_message_thread = Thread(target=receive_exchange_message_fcn, args=(self.message_queue, self.consumer, lambda: self.stop_flag,))
        # self.receive_exchange_message_thread = Thread(target=receive_exchange_message_fcn_local_test, args=(self.message_queue,))
        self.operator_exchange_message_thread = Thread(target=operate_exchange_message_fcn, args=(self.message_queue, self.event_manager, lambda: self.stop_flag,))

        self.event_manager.Start()
        self.logger.debug("ExchangeMessageManagement.initial returned.")

    def start(self):
        self.logger.debug("ExchangeMessageManagement.start is called.")
        self.receive_exchange_message_thread.start()
        self.operator_exchange_message_thread.start()
        self.logger.debug("ExchangeMessageManagement.start returned.")

    def stop(self):
        self.logger.debug("ExchangeMessageManagement.stop is called.")
        self.stop_flag = True
        self.event_manager.Stop()
        self.receive_exchange_message_thread.join()
        self.operator_exchange_message_thread.join()
        self.logger.debug("ExchangeMessageManagement.stop returned.")

    def delete(self):
        self.remove_listener_from_operator()

    def send_exchange_message(self, message):
        # if message not in self.exchange_message_operator.events:
        #     raise Exception(message + ' not in ' + self.exchange_message_operator.__class__.__name__ + '.events')

        self.producer.send(self.topic_send, bytes(message, encoding='utf-8'))
        self.logger.debug('send ' + message + '!')

    def add_listener_from_operator(self):
        self.exchange_message_operator.add_listener(self.event_manager)

    def remove_listener_from_operator(self):
        self.exchange_message_operator.remove_listener(self.event_manager)

