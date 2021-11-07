"""
@File:ProducerUsage.py
@Author:lcx
@Date:2020/10/209:35
@Desc:生产者用例
"""
import os
import time

from MessageQueue.exception.Exceptions import TopicNotAvailableException
from MessageQueue.implement.CommunicationInitial import CommunicationInitial
from MessageQueue.implement.CommunicationProducer import CommunicationProducer
if __name__ == '__main__':

    fatherPath = os.path.dirname(__file__)
    # 生产者配置文件地址
    # 配置文件中"bootstrap.servers"为必填选项，格式为"[host]:[port]"，请务必在本机系统中将服务器ip映射至host中，
    # host名称务必为“server”，不要直接使用ip访问！
    # 不清楚kafka服务器地址和端口时请询问kafka服务器维护者
    confPath = os.path.join(os.path.join(fatherPath, r"config"), 'producer-config.json')
    # 发信topic名
    topic = "py-test-topic1"
    # topic创建
    # topic与生产者之间不存在绑定关系，但建议使用者调用生产者向某topic发信前先进行topic创建
    # 该方法接受的第二个参数本应为CommunicatiognInitial类的配置文件，此处与CommunicationProducer类的配置文件通用
    # topicCreateResult = CommunicationInitial.topicCreate(topic, confPath)
    try:
        # 获得生产者实例
        producer = CommunicationProducer(confPath)
        # 连续发送五条消息
        # 生产者send方法接受的msg参数应为bytes型，本例仅使用bytes()方法给出简单的序列化示例，具体的序列化方式应由使用者决定
        for i in range(100):
            msg = bytes("msg{}".format(i), encoding="utf-8")
            sendResult = producer.send(topic, msg)
            print(sendResult)
            time.sleep(0.05)
        producer.close()
    except TopicNotAvailableException as e:
        print(e)
