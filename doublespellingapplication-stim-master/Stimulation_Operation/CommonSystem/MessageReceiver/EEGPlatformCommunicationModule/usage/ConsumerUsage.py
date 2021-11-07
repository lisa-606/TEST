"""
@File:ConsumerUsage.py
@Author:lcx
@Date:2020/10/209:35
@Desc:消费者用例
"""
import time

from CommonSystem.MessageReceiver.EEGPlatformCommunicationModule.exception.Exceptions import *
from CommonSystem.MessageReceiver.EEGPlatformCommunicationModule.implement.CommunicationConsumer import CommunicationConsumer
import uuid
if __name__ == '__main__':

    # 生产者配置文件地址
    # 配置文件中"bootstrap.servers"为必填选项，格式为"[kafka服务器ip]:[port]"，可以将服务器ip映射至host中，在[kafka服务器ip]中填入host名
    # 不清楚kafka服务器地址和端口时请询问kafka服务器维护者
    confPath = r"\CommonSystem\MessageReceiver\EEGPlatformCommunicationModule\usage\config\consumer-config.json"
    # 收信topic名
    topic = "py-test-topic1"

    try:
        # 获得消费者实例
        # 该构造方法的第二个参数为消费者组名，本项目内约定，非特殊声明时，消费者组名应与消费者实例一一对应，即不允许多个消费者使用同一消费者组名
        # 使用者可用UUID之类的唯一标识符做消费者组名

        consumer = CommunicationConsumer(confPath, str(uuid.uuid1()), topic)
        # 循环接收消息
        while True:
            # 收信方法调用，当消费者在0.5s时限内能收到的消息时，consumeMsg为bytes()型，本例仅使用str()方法给出简单的反序列化示例，具体反序列化
            # 方法应由使用者决定
            consumeMsg = consumer.receive()
            if consumeMsg:
                print(str(consumeMsg))
            else:
                print("no msg, get: {}".format(type(consumeMsg)))
            time.sleep(1)
    except TopicNotAvailableException as e:
        print(e)
