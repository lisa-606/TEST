#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
@Time : 2020/12/14 14:23
@Author : Nieeka
@Version：V 1.0
@File : ReceiverOperationMain.py
@Desciption :启动脚本
"""
import json
import time

from loguru import logger
from DeviceModule.NeuracleEEG_raw import NeuracleEEGThread
from MessageQueue.implement.CommunicationInitial import CommunicationInitial

if __name__ == '__main__':
    # Kafka_confPath = "/python_project/ReceiverOperation_bak/MessageQueue/usage/config/producer-config.json"#Linux
    Kafka_confPath = r".\MessageQueue\usage\config\producer-config.json"  # windows
    topic = 'NeuracleEEG_data'
    # NeuracleEEG_confPath = "/python_project/ReceiverOperation_bak/DeviceModule/config/NeuracleEEG.json"#linux
    NeuracleEEG_confPath = r".\DeviceModule\config\NeuracleEEG.json"  # windows
    with open(NeuracleEEG_confPath, 'r') as load_f:
        neuracle = json.load(fp=load_f)
    connecet_kafka = False
    while not connecet_kafka:
        try:
            topicCreateResult = CommunicationInitial.topicCreate(topic, Kafka_confPath)
            connecet_kafka = True
        except:
            logger.debug('can not connect kafkaserver')
            time.sleep(0.5)
    target_device = neuracle
    thread_data_server = NeuracleEEGThread(threadName='NeuracleEEG', device=target_device['device_name'],
                                           n_chan=target_device['n_chan'],
                                           hostname=target_device['hostname'], port=target_device['port'],
                                           srate=target_device['srate'], t_buffer=target_device['time_buffer'],
                                           topic=target_device['topic'])  # 建立线程

    thread_data_server.logger.info('!!!! The type of device you used is %s' % target_device['device_name'])
    thread_data_server.Daemon = True
    notconnect = thread_data_server.connect()
    if notconnect:
        thread_data_server.logger.debug("Can't connect recorder, Please open the hostport ")
        raise TypeError("Can't connect recorder, Please open the hostport ")
    else:
        thread_data_server.start()
