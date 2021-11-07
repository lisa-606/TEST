#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
@Time : 2021/5/31 15:00
@Author : Nieeka
@Version：V 1.0
@File : NeuracleEEGInterface.py
@Desciption :
"""
from abc import ABCMeta, abstractmethod


class NeuracleEEGInterface(metaclass=ABCMeta):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def read_thread(self):
        pass

    @abstractmethod
    def parse_data(self, raw):
        pass

    @abstractmethod
    def down_sample(self, data):
        pass
