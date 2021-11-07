"""
@File:ProducerUsage.py
@Author:lcx
@Date:2020/10/209:35
@Desc:生产者用例
"""
import time

from CommonSystem.MessageReceiver.EEGPlatformCommunicationModule.exception.Exceptions import *
from CommonSystem.MessageReceiver.EEGPlatformCommunicationModule.implement.CommunicationInitial import CommunicationInitial
from CommonSystem.MessageReceiver.EEGPlatformCommunicationModule.implement.CommunicationProducer import CommunicationProducer

if __name__ == '__main__':

    # 生产者配置文件地址
    # 配置文件中"bootstrap.servers"为必填选项，格式为"[kafka服务器ip]:[port]"，可以将服务器ip映射至host中，在[kafka服务器ip]中填入host名
    # 不清楚kafka服务器地址和端口时请询问kafka服务器维护者
    confPath = r"\CommonSystem\MessageReceiver\EEGPlatformCommunicationModule\usage\config\producer-config.json"
    # 发信topic名
    topic = "py-test-topic1"
    # topic创建
    # topic与生产者之间不存在绑定关系，但建议使用者调用生产者向某topic发信前先进行topic创建
    # 该方法接受的第二个参数本应为CommunicationInitial类的配置文件，此处与CommunicationProducer类的配置文件通用
    topicCreateResult = CommunicationInitial.topicCreate(topic, confPath)
    try:
        # 获得生产者实例
        producer = CommunicationProducer(confPath)
        # 连续发送五条消息
        # 生产者send方法接受的msg参数应为bytes型，本例仅使用bytes()方法给出简单的序列化示例，具体的序列化方式应由使用者决定
        for i in range(5):
            msg = bytes("msg{}".format(i), encoding="utf-8")
            producer.send(topic, msg)
            print(1)
            time.sleep(1)
        producer.close()
    except TopicNotAvailableException as e:
        print(e)
