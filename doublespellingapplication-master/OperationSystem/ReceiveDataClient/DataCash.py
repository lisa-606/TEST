#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
@Time : 2020/10/14 13:25
@Author : Nieeka
@Version：V 1.0
@File : DataCash.py
@Desciption :
"""
import threading
import time
import uuid
from collections import deque
import os

import numpy as np
import logging

# from doubleSpellingApplication.CommonSystem.Exceptions.CommunicationModuleExceptions import TopicNotAvailableException
from EEGPlatformCommunicationModule4py.communicationModuleImplement.CommunicationConsumer import CommunicationConsumer
from EEGPlatformCommunicationModule4py.communicationModuleInterface.communicationModuleException.Exceptions import TopicNotAvailableException

MaxValue = 20480

# father_path = os.path.dirname(__file__)
# filePath = r'consumer-config.json'
# confPath = os.path.join(father_path,filePath)
# confPath = r"..\CommonSystem\MessageReceiver\config\consumer-config.json"
confPath = os.path.join((os.path.dirname(os.path.dirname((os.path.dirname(__file__))))),
                        r"CommonSystem\MessageReceiver\config\consumer-config.json")
# print("configPath from datacash: "+confPath)

class DataCash(threading.Thread):

    def __init__(self, threadName, topic):
        threading.Thread.__init__(self)
        self.name = threadName
        self.topic = topic  # 实例所面对的topic
        self.messageQueue = deque(maxlen=MaxValue)  # 缓冲的数据队列
        # self.lock = threading.RLock()
        self.stop_flag = False
        self.channels = 10
        self.samples = 40
        # 获得消费者实例
        # 该构造方法的第二个参数为消费者组名，本项目内约定，非特殊声明时，消费者组名应与消费者实例一一对应，即不允许多个消费者使用同一消费者组名
        # 使用者可用UUID之类的唯一标识符做消费者组名
        self.consumer = CommunicationConsumer(confPath, str(uuid.uuid1()))
        self.consumer.subscribe(self.topic)

        self.logger = logging.getLogger("DoubleSpellingApplication.dataCash")

    def run(self):
        try:
            # 循环接收消息
            while True:
                consumeMsg = self.consumer.receive()
                self.logger.debug('datacache size: '+str(self.getMessageQueueSize()))
                # print('收到啦！', int(time.time() * 1000))
                if type(consumeMsg) == bytes:
                    # print(type(consumeMsg))
                    data = np.frombuffer(consumeMsg, dtype=np.float_)
                    data = data.reshape(self.channels, self.samples)
                    # print(data)
                    # self.lock.acquire()
                    self.messageQueue.append(data)
                    # self.lock.release()
                    # time.sleep(0.5)
                    # print(str(consumeMsg))
                # else:
                #     pass
                    # print("no msg, get: {}".format(type(consumeMsg)))
                if self.stop_flag:
                    self.logger.debug("Exiting dataCash")
                    break
                # time.sleep(1)
        except TopicNotAvailableException as e:
            self.logger.fatal(e, exc_info=True)
        # 从topic中获取数据
        # data = receive_from_topic(self.topic)
        # print(data)
        # self.lock.acquire()
        # self.messageQueue.append(data)
        # self.lock.release()

    def readData(self, startPoint, endPoint):
        if 0 <= startPoint < endPoint <= self.getMessageQueueSize():
            tmp = []
            # self.lock.acquire()
            for i in range(startPoint, endPoint):
                tmp.append(self.messageQueue[i])
            for j in tmp:
                self.messageQueue.remove(j)
            # self.lock.release()
            return tmp

    def readNewData(self, pointCount):
        return self.readData(self.getMessageQueueSize() - pointCount, self.getMessageQueueSize())

    def readFixedData(self, startPoint, length):
        return self.readData(startPoint, startPoint + length)

    def getMessageQueueSize(self):
        # self.lock.acquire()
        queue_len = len(self.messageQueue)
        # self.lock.release()
        return queue_len

    def clear(self):
        self.messageQueue.clear()


if __name__ == '__main__':

    # 收信topic名
    topic = 'NeuracleEEG_sy'
    NeuracleEEG_dataCash = DataCash('NeuracleEEG', topic)
    NeuracleEEG_dataCash.start()
    while 1:
        print(len(NeuracleEEG_dataCash.messageQueue))
        if len(NeuracleEEG_dataCash.messageQueue) > 1:
            print(NeuracleEEG_dataCash.readData(0, 1))

        time.sleep(0.5)
        # print(NeuracleEEG_dataCash.readData(0, 1))
    # try:
    #     # 获得消费者实例
    #     # 该构造方法的第二个参数为消费者组名，本项目内约定，非特殊声明时，消费者组名应与消费者实例一一对应，即不允许多个消费者使用同一消费者组名
    #     # 使用者可用UUID之类的唯一标识符做消费者组名
    #
    #     consumer = CommunicationConsumer(confPath, str(uuid.uuid1()), topic)
    #     # 循环接收消息
    #     while True:
    #         # 收信方法调用，当消费者在0.5s时限内能收到的消息时，consumeMsg为bytes()型，本例仅使用str()方法给出简单的反序列化示例，具体反序列化
    #         # 方法应由使用者决定
    #         consumeMsg = consumer.receive()
    #         if consumeMsg:
    #             print(str(consumeMsg))
    #         else:
    #             print("no msg, get: {}".format(type(consumeMsg)))
    #         time.sleep(1)
    # except TopicNotAvailableException as e:
    #     print(e)
