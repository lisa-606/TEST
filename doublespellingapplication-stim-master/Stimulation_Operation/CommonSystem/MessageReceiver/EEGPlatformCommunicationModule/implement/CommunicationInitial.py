"""
@File:CommunicationInitial.py
@Author:lcx
@Date:2020/10/714:38
@Desc:
"""
import datetime

from confluent_kafka.cimpl import KafkaException, KafkaError

from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.EEGPlatformCommunicationModule.interface.CommunicationInitialInterface import CommunicationInitialInterface
from confluent_kafka.admin import AdminClient, NewTopic
import json
import os
import time
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.EEGPlatformCommunicationModule.exception import Exceptions

class CommunicationInitial(CommunicationInitialInterface):

    @staticmethod
    def topicQuery(communicationCharactor):
        """

        :param communicationCharactor: a instance of class "CommunicationConsumer" or "CommunicationProducer"
        :return: a dict of futures for each topic, keyed by the topic name. type: dict(<topic_name, future>)
        """
        try:
            resultClusterMetadata = communicationCharactor.list_topics()
            return resultClusterMetadata
        except KafkaException as kafkae:
            raise Exceptions.TopicQueryFailed(kafkae)

    @staticmethod
    def topicCreate(topic, confPath, num_partitions=1, replication_factor=1):
        """

        :param topic: this param is the name of the topic that you want to create. type: str
        :param confPath: broker configuration, "bootstrap.servers" must be set
        :param num_partitions: this param is the partition number of the topic that you want to create.
        default: 1, type: int
        :param replication_factor: this param is the replication number of the topic that you want to create.
        default: 1, type: int
        :return: a dict of futures for each topic, keyed by the topic name. type: dict(<topic_name, future>)
        """
        if not os.path.exists(confPath):
            raise Exceptions.NoConfigFileException
        with open(confPath, 'r') as load_f:
            conf = json.load(load_f)
        if not "bootstrap.servers" in conf.keys():
            raise Exceptions.WrongConfigContextException
        adminClient = AdminClient(conf)
        new_topics = [NewTopic(topic, num_partitions, replication_factor)]
        fs = adminClient.create_topics(new_topics)
        print("create topic: "+str(datetime.datetime.now()))
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("create topic re: " + str(datetime.datetime.now()))
                return topic
            except KafkaException as ke:
                # topic slready exits.
                if ke.args[0].code == 37:
                    return topic
            except Exception as e:
                # print("Failed to create topic {}: {}".format(topic, e))
                raise Exceptions.TopicCreateFailed(e)

    @staticmethod
    def topicDelete(topic, confPath):
        """

        :param topic: this param is the name of the topic that you want to create. type: str
        :param confPath: broker configuration, "bootstrap.servers" must be set
        :return: a dict of futures for each topic, keyed by the topic name. type: dict(<topic_name, future>)
        """
        if not os.path.exists(confPath):
            raise Exceptions.NoConfigFileException
        with open(confPath, 'r') as load_f:
            conf = json.load(load_f)
        if not "bootstrap.servers" in conf.keys():
            raise Exceptions.WrongConfigContextException
        adminClient = AdminClient(conf)
        fs = adminClient.delete_topics([topic], request_timeout=1)
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                return topic
            except Exception as e:
                # print("Failed to delete topic {}: {}".format(topic, e))
                raise Exceptions.TopicDeleteFailed(e)
