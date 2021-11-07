"""
@File:CommunicationProducerInterface.py
@Author:lcx
@Date:2020/10/714:37
@Desc:
"""
from abc import ABCMeta, abstractmethod
class CommunicationProducerInterface(metaclass=ABCMeta):

    @abstractmethod
    def list_topics(self, topic=None, timeout=0.5):
        pass

    @abstractmethod
    def send(self, topic, value, key=None):
        pass

    @abstractmethod
    def close(self):
        pass
