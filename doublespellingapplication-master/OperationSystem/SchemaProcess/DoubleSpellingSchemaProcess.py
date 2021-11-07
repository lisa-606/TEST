from doubleSpellingApplication.OperationSystem.SchemaProcess.BasicSchemaProcess import BasicSchemaProcess
from doubleSpellingApplication.OperationSystem.AnalysisProcess.ValueObj.AnalysisProcessUpdataObj import AnalysisProcessUpdataObj
from doubleSpellingApplication.OperationSystem.AnalysisProcess.ValueObj.DownListObj import DownListObj
from doubleSpellingApplication.OperationSystem.ShuangPinAPI.Utils import IDTableLoader
from doubleSpellingApplication.OperationSystem.ShuangPinAPI.DoubleSpellingInputMethodImpl import DoubleSpellingInputMethodImpl
from doubleSpellingApplication.OperationSystem.ShuangPinAPI.pinyin2ID import pinyin2ID
from EEGPlatformCommunicationModule4py.communicationModuleImplement.CommunicationProducer import CommunicationProducer
from EEGPlatformCommunicationModule4py.communicationModuleImplement.CommunicationInitial import CommunicationInitial
from persistentModel2py.doubleSpellingRecordModel import DoubleSpellingRecordModel
import json
import datetime
import numpy as np
import socket
import time
import copy
import os
import logging

initial_config_path = os.path.join((os.path.dirname(os.path.dirname((os.path.dirname(__file__))))),
                        r"CommonSystem\MessageReceiver\config\Initial-config.json")

producer_config_path = os.path.join((os.path.dirname(os.path.dirname((os.path.dirname(__file__))))),
                        r"CommonSystem\MessageReceiver\config\producer-config.json")


class DoubleSpellingSchemaProcess(BasicSchemaProcess):
    def __init__(self):
        super(BasicSchemaProcess, self).__init__()

        self.mode = None

        # 模式信息
        self.schema_process_information = None

        # 字母表
        # {'ID', 'UAVCOMMANDID', 'DISPLAYCHAR', 'FREQUENCY', 'PHASE'}
        self.target_table = None

        # 实验信息
        self.experiment_information = None

        self.target_template_set = None

        self.exchange_message_management = None

        self.uav_connector = None

        # 准备阶段时间
        self.prepare_last_time = None

        # 休息时间
        self.finish_last_time = None

        self.up_text = None

        self.down_text = None

        self.down_list = None

        self.shengmuyunmu_to_get_candidate_hanzi = None

        self.candidate_hanzi = None

        self.candidate_hanzi_display = None

        self.candidate_hanzi_id_array = None

        self.candidate_hanzi_display_id_array = None

        self.page = None

        self.max_page = None

        # self.enter_flag = None

        self.enter_counter = None

        self.fake_producer_topic = 'stim_to_ope_suyan'

        self.fake_strd_producer = CommunicationProducer(producer_config_path)

        self.logger = logging.getLogger("DoubleSpellingApplication.DoubleSpellingSchemaProcess")

        self.speak = None

        self.persistent_topic = None

        self.doubleSpellingRecordModel = None

    def initial(self, experiment_information, exchange_message_management):
        # 初始化控制器
        BasicSchemaProcess.initial(self)

        # 初始化基准参数
        self.mode = 0

        self.experiment_information = experiment_information

        self.schema_process_information = experiment_information.schema_process_information

        self.target_table = self.schema_process_information.target_table

        self.exchange_message_management = exchange_message_management

        # 准备阶段时间
        self.prepare_last_time = experiment_information.prepare_last_time

        # 休息时间
        self.finish_last_time = experiment_information.finish_last_time

        # 候选字符

        self.target_template_set = self.create_target_template_set(self.target_table[0])

        self.up_text = ''

        self.down_text = ''

        self.down_list = []

        self.clear()

        self.candidate_hanzi_display = self.candidate_display_reorder(self.candidate_hanzi_display)

        self.candidate_hanzi_display_id_array = self.candidate_display_reorder(self.candidate_hanzi_display_id_array)

        # self.enter_flag = 0

        self.enter_counter = 0

        self.speak = 0

        self.converter = DoubleSpellingInputMethodImpl(2, 5)

        # self.IDTable = IDTableLoader(r'ShuangPinAPI/IDTable.csv')
        self.IDTable = IDTableLoader(os.path.join((os.path.dirname(os.path.dirname((os.path.dirname(__file__))))),
                     r"OperationSystem\ShuangPinAPI\IDTable.csv"))

        self.fre_dict = {
            'a': {'a': 132, 'an': 739, 'i': 0, 'u': 0, 'o': 0, 'uo': 0, 'ua': 0, 'ang': 34, 'ie': 0, 'ou': 0, 'er': 0,
                  'ei': 0, 'ai': 440, 'e': 0, 'en': 0, 'ing': 0, 'ong': 0, 'ao': 167, 'iao': 0, 'ian': 0, 'iu': 0,
                  'eng': 0,
                  'iang': 0, 'in': 0, 'un': 0, 'ia': 0, 'ui': 0, 'uang': 0, 'v': 0, 'uan': 0, 'iong': 0, 'ue': 0,
                  'uai': 0,
                  've': 0, 'n': 0},
            'b': {'a': 690, 'an': 1410, 'i': 1205, 'u': 2976, 'o': 686, 'uo': 0, 'ua': 0, 'ang': 351, 'ie': 158,
                  'ou': 0,
                  'er': 0, 'ei': 793, 'ai': 1054, 'e': 0, 'en': 395, 'ing': 980, 'ong': 0, 'ao': 1399, 'iao': 463,
                  'ian': 778,
                  'iu': 0, 'eng': 94, 'iang': 0, 'in': 114, 'un': 0, 'ia': 0, 'ui': 0, 'uang': 0, 'v': 0, 'uan': 0,
                  'iong': 0,
                  'ue': 0, 'uai': 0, 've': 0, 'n': 0},
            'd': {'a': 1931, 'an': 1148, 'i': 1487, 'u': 964, 'o': 0, 'uo': 446, 'ua': 0, 'ang': 472, 'ie': 157,
                  'ou': 453,
                  'er': 0, 'ei': 0, 'ai': 839, 'e': 727, 'en': 0, 'ing': 1555, 'ong': 1209, 'ao': 1688, 'iao': 356,
                  'ian': 1426, 'iu': 26, 'eng': 436, 'iang': 0, 'in': 0, 'un': 152, 'ia': 0, 'ui': 418, 'uang': 0,
                  'v': 0,
                  'uan': 689, 'iong': 0, 'ue': 0, 'uai': 0, 've': 0, 'n': 0},
            'y': {'a': 1029, 'an': 2127, 'i': 4728, 'u': 1924, 'o': 6, 'uo': 0, 'ua': 0, 'ang': 1116, 'ie': 0,
                  'ou': 1802,
                  'er': 0, 'ei': 0, 'ai': 0, 'e': 1317, 'en': 0, 'ing': 1034, 'ong': 914, 'ao': 879, 'iao': 0, 'ian': 0,
                  'iu': 0, 'eng': 0, 'iang': 0, 'in': 1274, 'un': 556, 'ia': 0, 'ui': 0, 'uang': 0, 'v': 0, 'uan': 1509,
                  'iong': 0, 'ue': 512, 'uai': 0, 've': 0, 'n': 0},
            'l': {'a': 363, 'an': 419, 'i': 2696, 'u': 1073, 'o': 0, 'uo': 609, 'ua': 0, 'ang': 242, 'ie': 371,
                  'ou': 266,
                  'er': 0, 'ei': 413, 'ai': 412, 'e': 709, 'en': 0, 'ing': 676, 'ong': 299, 'ao': 664, 'iao': 801,
                  'ian': 828,
                  'iu': 1026, 'eng': 218, 'iang': 830, 'in': 493, 'un': 356, 'ia': 5, 'ui': 0, 'uang': 0, 'v': 633,
                  'uan': 254, 'iong': 0, 'ue': 0, 'uai': 0, 've': 3, 'n': 0},
            'j': {'a': 0, 'an': 0, 'i': 4563, 'u': 1088, 'o': 0, 'uo': 0, 'ua': 0, 'ang': 0, 'ie': 2131, 'ou': 0,
                  'er': 0,
                  'ei': 0, 'ai': 0, 'e': 0, 'en': 0, 'ing': 2433, 'ong': 0, 'ao': 0, 'iao': 1931, 'ian': 2601,
                  'iu': 973,
                  'eng': 0, 'iang': 672, 'in': 1584, 'un': 625, 'ia': 1806, 'ui': 0, 'uang': 0, 'v': 0, 'uan': 170,
                  'iong': 25, 'ue': 421, 'uai': 0, 've': 0, 'n': 0},
            'h': {'a': 81, 'an': 615, 'i': 0, 'u': 1049, 'o': 0, 'uo': 1000, 'ua': 1855, 'ang': 108, 'ie': 0, 'ou': 716,
                  'er': 0, 'ei': 203, 'ai': 678, 'e': 1787, 'en': 105, 'ing': 0, 'ong': 573, 'ao': 791, 'iao': 0,
                  'ian': 0,
                  'iu': 0, 'eng': 219, 'iang': 0, 'in': 0, 'un': 317, 'ia': 0, 'ui': 1302, 'uang': 560, 'v': 0,
                  'uan': 697,
                  'iong': 0, 'ue': 0, 'uai': 150, 've': 0, 'n': 0},
            'zh': {'a': 284, 'an': 710, 'i': 4673, 'u': 1604, 'o': 0, 'uo': 161, 'ua': 46, 'ang': 1059, 'ie': 0,
                   'ou': 472,
                   'er': 0, 'ei': 0, 'ai': 199, 'e': 710, 'en': 942, 'ing': 0, 'ong': 1701, 'ao': 422, 'iao': 0,
                   'ian': 0,
                   'iu': 0, 'eng': 1120, 'iang': 0, 'in': 0, 'un': 119, 'ia': 0, 'ui': 155, 'uang': 593, 'v': 0,
                   'uan': 500,
                   'iong': 0, 'ue': 0, 'uai': 3, 've': 0, 'n': 0},
            'ch': {'a': 950, 'an': 456, 'i': 731, 'u': 1545, 'o': 0, 'uo': 30, 'ua': 0, 'ang': 922, 'ie': 0, 'ou': 330,
                   'er': 0, 'ei': 0, 'ai': 109, 'e': 439, 'en': 400, 'ing': 0, 'ong': 404, 'ao': 489, 'iao': 0,
                   'ian': 0,
                   'iu': 0, 'eng': 1174, 'iang': 0, 'in': 0, 'un': 364, 'ia': 0, 'ui': 453, 'uang': 385, 'v': 0,
                   'uan': 616,
                   'iong': 0, 'ue': 0, 'uai': 16, 've': 0, 'n': 0},
            'z': {'a': 169, 'an': 71, 'i': 2845, 'u': 665, 'o': 0, 'uo': 705, 'ua': 0, 'ang': 150, 'ie': 0, 'ou': 186,
                  'er': 0, 'ei': 40, 'ai': 572, 'e': 221, 'en': 120, 'ing': 0, 'ong': 359, 'ao': 595, 'iao': 0,
                  'ian': 0,
                  'iu': 0, 'eng': 143, 'iang': 0, 'in': 0, 'un': 61, 'ia': 0, 'ui': 343, 'uang': 0, 'v': 0, 'uan': 49,
                  'iong': 0, 'ue': 0, 'uai': 0, 've': 0, 'n': 0},
            'e': {'a': 0, 'an': 0, 'i': 0, 'u': 0, 'o': 0, 'uo': 0, 'ua': 0, 'ang': 0, 'ie': 0, 'ou': 0, 'er': 1781,
                  'ei': 1,
                  'ai': 0, 'e': 382, 'en': 52, 'ing': 0, 'ong': 0, 'ao': 0, 'iao': 0, 'ian': 0, 'iu': 0, 'eng': 0,
                  'iang': 0,
                  'in': 0, 'un': 0, 'ia': 0, 'ui': 0, 'uang': 0, 'v': 0, 'uan': 0, 'iong': 0, 'ue': 0, 'uai': 0,
                  've': 0,
                  'n': 0},
            'n': {'a': 375, 'an': 452, 'i': 700, 'u': 112, 'o': 0, 'uo': 55, 'ua': 0, 'ang': 407, 'ie': 114, 'ou': 0,
                  'er': 0,
                  'ei': 674, 'ai': 145, 'e': 98, 'en': 24, 'ing': 204, 'ong': 311, 'ao': 357, 'iao': 437, 'ian': 506,
                  'iu': 222, 'eng': 297, 'iang': 66, 'in': 2, 'un': 0, 'ia': 0, 'ui': 0, 'uang': 0, 'v': 189, 'uan': 54,
                  'iong': 0, 'ue': 0, 'uai': 0, 've': 5, 'n': 4},
            's': {'a': 102, 'an': 588, 'i': 1350, 'u': 796, 'o': 0, 'uo': 667, 'ua': 0, 'ang': 119, 'ie': 0, 'ou': 44,
                  'er': 0, 'ei': 0, 'ai': 222, 'e': 419, 'en': 34, 'ing': 0, 'ong': 334, 'ao': 114, 'iao': 0, 'ian': 0,
                  'iu': 0, 'eng': 15, 'iang': 0, 'in': 0, 'un': 157, 'ia': 0, 'ui': 408, 'uang': 0, 'v': 0, 'uan': 465,
                  'iong': 0, 'ue': 0, 'uai': 0, 've': 0, 'n': 0},
            'sh': {'a': 437, 'an': 785, 'i': 5478, 'u': 4397, 'o': 0, 'uo': 350, 'ua': 77, 'ang': 1101, 'ie': 0,
                   'ou': 1549,
                   'er': 0, 'ei': 29, 'ai': 57, 'e': 866, 'en': 1399, 'ing': 0, 'ong': 0, 'ao': 321, 'iao': 0, 'ian': 0,
                   'iu': 0, 'eng': 1716, 'iang': 0, 'in': 0, 'un': 129, 'ia': 0, 'ui': 1007, 'uang': 289, 'v': 0,
                   'uan': 91,
                   'iong': 0, 'ue': 0, 'uai': 85, 've': 0, 'n': 0},
            'm': {'a': 723, 'an': 320, 'i': 516, 'u': 795, 'o': 961, 'uo': 0, 'ua': 0, 'ang': 146, 'ie': 112, 'ou': 95,
                  'er': 0, 'ei': 907, 'ai': 712, 'e': 299, 'en': 529, 'ing': 934, 'ong': 0, 'ao': 545, 'iao': 216,
                  'ian': 894,
                  'iu': 19, 'eng': 291, 'iang': 0, 'in': 391, 'un': 0, 'ia': 0, 'ui': 0, 'uang': 0, 'v': 0, 'uan': 0,
                  'iong': 0, 'ue': 0, 'uai': 0, 've': 0, 'n': 0},
            't': {'a': 144, 'an': 620, 'i': 1167, 'u': 850, 'o': 0, 'uo': 425, 'ua': 0, 'ang': 411, 'ie': 377,
                  'ou': 1076,
                  'er': 0, 'ei': 0, 'ai': 811, 'e': 215, 'en': 0, 'ing': 420, 'ong': 1380, 'ao': 444, 'iao': 315,
                  'ian': 901,
                  'iu': 0, 'eng': 109, 'iang': 0, 'in': 0, 'un': 62, 'ia': 0, 'ui': 311, 'uang': 0, 'v': 0, 'uan': 164,
                  'iong': 0, 'ue': 0, 'uai': 0, 've': 0, 'n': 0},
            'f': {'a': 1017, 'an': 951, 'i': 0, 'u': 2369, 'o': 0, 'uo': 0, 'ua': 0, 'ang': 1210, 'ie': 0, 'ou': 23,
                  'er': 0,
                  'ei': 877, 'ai': 0, 'e': 0, 'en': 978, 'ing': 0, 'ong': 0, 'ao': 0, 'iao': 0, 'ian': 0, 'iu': 0,
                  'eng': 1125, 'iang': 0, 'in': 0, 'un': 0, 'ia': 0, 'ui': 0, 'uang': 0, 'v': 0, 'uan': 0, 'iong': 0,
                  'ue': 0,
                  'uai': 0, 've': 0, 'n': 0},
            'g': {'a': 35, 'an': 906, 'i': 0, 'u': 2239, 'o': 0, 'uo': 1030, 'ua': 284, 'ang': 614, 'ie': 0, 'ou': 407,
                  'er': 0, 'ei': 82, 'ai': 300, 'e': 887, 'en': 300, 'ing': 0, 'ong': 1973, 'ao': 857, 'iao': 0,
                  'ian': 0,
                  'iu': 0, 'eng': 181, 'iang': 0, 'in': 0, 'un': 100, 'ia': 0, 'ui': 633, 'uang': 689, 'v': 0,
                  'uan': 2105,
                  'iong': 0, 'ue': 0, 'uai': 109, 've': 0, 'n': 0},
            'k': {'a': 138, 'an': 291, 'i': 0, 'u': 387, 'o': 0, 'uo': 218, 'ua': 64, 'ang': 457, 'ie': 0, 'ou': 638,
                  'er': 0,
                  'ei': 0, 'ai': 626, 'e': 1366, 'en': 64, 'ing': 0, 'ong': 548, 'ao': 154, 'iao': 0, 'ian': 0, 'iu': 0,
                  'eng': 47, 'iang': 0, 'in': 0, 'un': 98, 'ia': 0, 'ui': 209, 'uang': 281, 'v': 0, 'uan': 291,
                  'iong': 0,
                  'ue': 0, 'uai': 207, 've': 0, 'n': 0},
            'r': {'a': 0, 'an': 475, 'i': 312, 'u': 889, 'o': 0, 'uo': 82, 'ua': 0, 'ang': 103, 'ie': 0, 'ou': 194,
                  'er': 0,
                  'ei': 0, 'ai': 0, 'e': 329, 'en': 1759, 'ing': 0, 'ong': 459, 'ao': 119, 'iao': 0, 'ian': 0, 'iu': 0,
                  'eng': 11, 'iang': 0, 'in': 0, 'un': 61, 'ia': 0, 'ui': 58, 'uang': 0, 'v': 0, 'uan': 142, 'iong': 0,
                  'ue': 0, 'uai': 0, 've': 0, 'n': 0},
            'w': {'a': 163, 'an': 792, 'i': 0, 'u': 2361, 'o': 696, 'uo': 0, 'ua': 0, 'ang': 627, 'ie': 0, 'ou': 0,
                  'er': 0,
                  'ei': 2120, 'ai': 660, 'e': 0, 'en': 945, 'ing': 0, 'ong': 0, 'ao': 0, 'iao': 0, 'ian': 0, 'iu': 0,
                  'eng': 31, 'iang': 0, 'in': 0, 'un': 0, 'ia': 0, 'ui': 0, 'uang': 0, 'v': 0, 'uan': 0, 'iong': 0,
                  'ue': 0,
                  'uai': 0, 've': 0, 'n': 0},
            'q': {'a': 0, 'an': 0, 'i': 2977, 'u': 1053, 'o': 0, 'uo': 0, 'ua': 0, 'ang': 0, 'ie': 636, 'ou': 0,
                  'er': 0,
                  'ei': 0, 'ai': 0, 'e': 0, 'en': 0, 'ing': 1317, 'ong': 0, 'ao': 0, 'iao': 364, 'ian': 1094, 'iu': 609,
                  'eng': 0, 'iang': 655, 'in': 381, 'un': 134, 'ia': 52, 'ui': 0, 'uang': 0, 'v': 0, 'uan': 817,
                  'iong': 121,
                  'ue': 203, 'uai': 0, 've': 0, 'n': 0},
            'p': {'a': 99, 'an': 301, 'i': 783, 'u': 418, 'o': 344, 'uo': 0, 'ua': 0, 'ang': 104, 'ie': 12, 'ou': 92,
                  'er': 0,
                  'ei': 311, 'ai': 386, 'e': 0, 'en': 122, 'ing': 608, 'ong': 0, 'ao': 299, 'iao': 215, 'ian': 614,
                  'iu': 0,
                  'eng': 195, 'iang': 0, 'in': 455, 'un': 0, 'ia': 0, 'ui': 0, 'uang': 0, 'v': 0, 'uan': 0, 'iong': 0,
                  'ue': 0, 'uai': 0, 've': 0, 'n': 0},
            'c': {'a': 45, 'an': 423, 'i': 1188, 'u': 193, 'o': 0, 'uo': 186, 'ua': 0, 'ang': 204, 'ie': 0, 'ou': 38,
                  'er': 0,
                  'ei': 0, 'ai': 693, 'e': 894, 'en': 8, 'ing': 0, 'ong': 234, 'ao': 400, 'iao': 0, 'ian': 0, 'iu': 0,
                  'eng': 179, 'iang': 0, 'in': 0, 'un': 260, 'ia': 0, 'ui': 140, 'uang': 0, 'v': 0, 'uan': 39,
                  'iong': 0,
                  'ue': 0, 'uai': 0, 've': 0, 'n': 0},
            'x': {'a': 0, 'an': 0, 'i': 2321, 'u': 498, 'o': 0, 'uo': 0, 'ua': 0, 'ang': 0, 'ie': 703, 'ou': 0, 'er': 0,
                  'ei': 0, 'ai': 0, 'e': 0, 'en': 0, 'ing': 2948, 'ong': 0, 'ao': 0, 'iao': 1432, 'ian': 1977,
                  'iu': 661,
                  'eng': 0, 'iang': 1550, 'in': 1681, 'un': 354, 'ia': 825, 'ui': 0, 'uang': 0, 'v': 0, 'uan': 427,
                  'iong': 439, 'ue': 1561, 'uai': 0, 've': 0, 'n': 0},
            'o': {'a': 0, 'an': 0, 'i': 0, 'u': 0, 'o': 11, 'uo': 0, 'ua': 0, 'ang': 0, 'ie': 0, 'ou': 100, 'er': 0,
                  'ei': 0,
                  'ai': 0, 'e': 0, 'en': 0, 'ing': 0, 'ong': 0, 'ao': 0, 'iao': 0, 'ian': 0, 'iu': 0, 'eng': 0,
                  'iang': 0,
                  'in': 0, 'un': 0, 'ia': 0, 'ui': 0, 'uang': 0, 'v': 0, 'uan': 0, 'iong': 0, 'ue': 0, 'uai': 0,
                  've': 0,
                  'n': 0}
        }

        self.doubleSpellingRecordModel = DoubleSpellingRecordModel()

        self.persistent_topic = "persistent-test"

        topicCreateResult = CommunicationInitial.topicCreate(self.persistent_topic, initial_config_path)
        self.persistent_producer = CommunicationProducer(producer_config_path)

    def get_analysis_updata_obj(self):
        analysis_process_updata_obj = AnalysisProcessUpdataObj()
        analysis_process_updata_obj.target_template_set = self.target_template_set
        return analysis_process_updata_obj

    def clear(self):
        self.shengmuyunmu_to_get_candidate_hanzi = []
        self.candidate_hanzi = [',', '.', ';', ':', "'", '"', '!', '`', '@', '(', ')']
        self.candidate_hanzi_display = ['上', ',', '.', ';', ':', "'", '"', '!', '`', '下']
        self.candidate_hanzi_id_array = ['', '', '', '', '', '', '', '', '', '', '']
        self.candidate_hanzi_display_id_array = ['', '', '', '', '', '', '', '', '', '']
        self.page = 0
        self.max_page = 1

    def prepare(self):
        pass

    def over(self):
        pass

    def report(self, result_index):
        self.speak = 0
        result_index = int(result_index)

        if self.count_character_num() >= 40 and (result_index not in [0,2,4,6,8,16,18,28,30,36,37]):
            return

        self.candidate_hanzi_display = self.candidate_display_reorder_reverse(self.candidate_hanzi_display)
        self.candidate_hanzi_display_id_array = self.candidate_display_reorder_reverse(
            self.candidate_hanzi_display_id_array)

        result_char = self.target_table[self.mode]['DISPLAYCHAR'][result_index]
        # result_obj = DownListObj(result_char)
        # 识别结果
        self.logger.debug('\n{0}.report:本次识别结果{1}，刺激频率{2}，执行时间{3}\n'.format(self.__class__.__name__,
                                                                self.target_table[self.mode]['DISPLAYCHAR'][result_index],
                                                                self.target_table[self.mode]['FREQUENCY'][result_index],
                                                                datetime.datetime.now()))



        # result_obj = self.recongize(result_id)
        if self.mode == 0 or self.mode == 1:
            result_obj = DownListObj(result_char, 'CH')

            if result_obj.is_punctuation:
                self.enter_counter = 0
                if len(self.down_list) != 0:
                    if self.down_list[-1].language == 'CH' and self.down_list[-1].is_shengmuyunmu:
                    # if self.down_list[len(self.down_list)-1].is_shengmuyunmu:
                        self.candidate_hanzi_display = self.candidate_display_reorder(self.candidate_hanzi_display)
                        self.candidate_hanzi_display_id_array = self.candidate_display_reorder(
                            self.candidate_hanzi_display_id_array)
                        self.fake_strd_producer.send(self.fake_producer_topic, bytes('STRD', encoding='utf-8'))
                        return
                self.down_list.append(result_obj)
                # self.down_text = ''.join(i.char for i in self.down_list)
                self.get_down_text()

            elif result_obj.char == '<--':
                self.enter_counter = 0
                if len(self.down_list) != 0:

                    if self.down_list[-1].language == 'EN':
                        self.down_list = self.down_list[0:-1]
                        # self.mode = 0
                    else:
                        if not self.down_list[-1].is_shengmuyunmu:
                            if len(self.down_list[-1].char) > 1:
                                self.down_list[-1].char = self.down_list[-1].char[0:-1]
                            else:
                                self.down_list = self.down_list[0:-1]
                        elif self.down_list[-1].is_shengmu:
                            self.down_list = self.down_list[0:-1]
                            self.shengmuyunmu_to_get_candidate_hanzi = self.shengmuyunmu_to_get_candidate_hanzi[0:-1]
                            self.mode = 0
                        else:
                            self.down_list = self.down_list[0:-1]
                            self.shengmuyunmu_to_get_candidate_hanzi = self.shengmuyunmu_to_get_candidate_hanzi[0:-1]
                            self.mode = 1

                    if len(self.shengmuyunmu_to_get_candidate_hanzi) != 0:
                        idArray = pinyin2ID(self.shengmuyunmu_to_get_candidate_hanzi, self.IDTable)
                        ch = self.converter.getCandidateChar(idArray)
                        self.candidate_hanzi = ch.character
                        self.candidate_hanzi_id_array = ch.idArray
                        if len(self.candidate_hanzi) < 8:
                            self.max_page = 0
                            self.candidate_hanzi_display[1:len(self.candidate_hanzi) + 1] = self.candidate_hanzi[
                                                                                            0: len(self.candidate_hanzi)]
                            for i in range(len(self.candidate_hanzi) + 1, 9):
                                self.candidate_hanzi_display[i] = ''
                            self.candidate_hanzi_display_id_array[
                            1:len(self.candidate_hanzi) + 1] = self.candidate_hanzi_id_array[0: len(self.candidate_hanzi)]
                        else:
                            self.max_page = int(len(self.candidate_hanzi) / 8)
                            self.candidate_hanzi_display[1:9] = self.candidate_hanzi[0:8]
                            self.candidate_hanzi_display_id_array[1:9] = self.candidate_hanzi_id_array[0:8]
                    else:
                        self.clear()
                # self.down_text = ''.join(i.char for i in self.down_list)
                self.get_down_text()

            elif result_obj.char == '<-┘':

                if len(self.down_list) == 0:
                    self.candidate_hanzi_display = self.candidate_display_reorder(self.candidate_hanzi_display)
                    self.candidate_hanzi_display_id_array = self.candidate_display_reorder(
                        self.candidate_hanzi_display_id_array)
                    self.fake_strd_producer.send(self.fake_producer_topic, bytes('STRD', encoding='utf-8'))
                    self.enter_counter = 0
                    return

                self.enter_counter += 1
                if self.enter_counter == 1 and (self.down_list[-1].language == 'CH' and self.down_list[-1].is_shengmuyunmu):
                    self.del_shengmuyunmu()
                    self.mode = 0

                elif self.enter_counter == 2:
                    # self.up_text = self.up_text + ''.join(i.char for i in self.down_list)
                    self.up_text = ''.join(i.char for i in self.down_list)
                    self.down_list = []
                    self.down_text = ''
                    self.enter_counter = 0
                    self.clear()
                    self.speak = 1
                    self.doubleSpellingRecordModel.setTime(int(round(time.time() * 1000)))
                    self.doubleSpellingRecordModel.setContent(self.up_text)
                    msg = self.doubleSpellingRecordModel.serialize()
                    self.persistent_producer.send(self.persistent_topic, msg)

            elif result_obj.is_shengmuyunmu:
                self.enter_counter = 0
                if result_obj.is_yunmu and self.mode == 1:

                    sm = self.shengmuyunmu_to_get_candidate_hanzi[-1]
                    if result_obj.char.find('\n') > 0:
                        yunmu = result_obj.char.split('\n')
                        yunmu1 = yunmu[0]
                        yunmu2 = yunmu[1]

                        if self.is_correct_yunmu(sm, yunmu1):
                            result_obj.char = yunmu1
                        elif self.is_correct_yunmu(sm, yunmu2):
                            result_obj.char = yunmu2
                        else:
                            self.candidate_hanzi_display = self.candidate_display_reorder(self.candidate_hanzi_display)
                            self.candidate_hanzi_display_id_array = self.candidate_display_reorder(
                                self.candidate_hanzi_display_id_array)
                            self.fake_strd_producer.send(self.fake_producer_topic, bytes('STRD', encoding='utf-8'))
                            return

                    else:

                        if not self.is_correct_yunmu(sm, result_obj.char):
                            self.candidate_hanzi_display = self.candidate_display_reorder(self.candidate_hanzi_display)
                            self.candidate_hanzi_display_id_array = self.candidate_display_reorder(
                                self.candidate_hanzi_display_id_array)
                            self.fake_strd_producer.send(self.fake_producer_topic, bytes('STRD', encoding='utf-8'))
                            return

                self.switch_mode_ch()
                self.down_list.append(result_obj)

                self.get_down_text()

                self.shengmuyunmu_to_get_candidate_hanzi.append(result_obj.char)
                idArray = pinyin2ID(self.shengmuyunmu_to_get_candidate_hanzi, self.IDTable)
                ch = self.converter.getCandidateChar(idArray)
                self.candidate_hanzi = ch.character
                self.candidate_hanzi_id_array = ch.idArray
                if len(self.candidate_hanzi) < 8:
                    self.max_page = 0
                    self.candidate_hanzi_display[1:len(self.candidate_hanzi) + 1] = self.candidate_hanzi[0 : len(self.candidate_hanzi)]
                    for i in range(len(self.candidate_hanzi) + 1, 9):
                        self.candidate_hanzi_display[i] = ''
                    self.candidate_hanzi_display_id_array[1:len(self.candidate_hanzi) + 1] = self.candidate_hanzi_id_array[0 : len(self.candidate_hanzi)]
                else:
                    self.max_page = int(len(self.candidate_hanzi)/8)
                    self.candidate_hanzi_display[1:9] = self.candidate_hanzi[0:8]
                    self.candidate_hanzi_display_id_array[1:9] = self.candidate_hanzi_id_array[0:8]

            elif result_obj.char == '切换':
                self.enter_counter = 0
                self.del_shengmuyunmu()
                self.candidate_hanzi = []
                self.candidate_hanzi_display = ['', '', '', '', '', '', '', '', '', '']
                self.candidate_hanzi_id_array = []
                self.candidate_hanzi_display_id_array = ['', '', '', '', '', '', '', '', '', '']
                self.max_page = 0
                self.mode = 2

            else:  # [0,2,4,6,8,16,18,28,30,36]
                self.enter_counter = 0
                if result_index is 30:
                    if self.page is 0:
                        self.candidate_hanzi_display = self.candidate_display_reorder(self.candidate_hanzi_display)
                        self.candidate_hanzi_display_id_array = self.candidate_display_reorder(
                            self.candidate_hanzi_display_id_array)
                        self.fake_strd_producer.send(self.fake_producer_topic, bytes('STRD', encoding='utf-8'))
                        return
                    else:
                        self.page -= 1
                        # self.candidate_hanzi_display = self.candidate_display_reorder_reverse(self.candidate_hanzi_display)
                        # self.candidate_hanzi_display_id_array = self.candidate_display_reorder_reverse(self.candidate_hanzi_display_id_array)
                        self.candidate_hanzi_display[1:9] = self.candidate_hanzi[8*self.page : 8*(1+self.page)]
                        self.candidate_hanzi_display_id_array[1:9] = self.candidate_hanzi_id_array[8 * self.page : 8 * (1 + self.page)]

                elif result_index is 36:
                    if self.page == self.max_page:
                        self.candidate_hanzi_display = self.candidate_display_reorder(self.candidate_hanzi_display)
                        self.candidate_hanzi_display_id_array = self.candidate_display_reorder(
                            self.candidate_hanzi_display_id_array)
                        self.fake_strd_producer.send(self.fake_producer_topic, bytes('STRD', encoding='utf-8'))
                        return
                    else:
                        self.page += 1
                        # self.candidate_hanzi_display = self.candidate_display_reorder_reverse(self.candidate_hanzi_display)
                        # self.candidate_hanzi_display_id_array = self.candidate_display_reorder_reverse(self.candidate_hanzi_display_id_array)

                        if self.page == self.max_page:
                            self.candidate_hanzi_display[1 : len(self.candidate_hanzi)%8+1] = self.candidate_hanzi[8 * self.page:]
                            self.candidate_hanzi_display[len(self.candidate_hanzi) % 8 + 1 : 9] = ['' for i in range(0, 8 - len(self.candidate_hanzi) % 8)]

                            self.candidate_hanzi_display_id_array[1: len(self.candidate_hanzi) % 8 + 1] = self.candidate_hanzi_id_array[8 * self.page:]
                            self.candidate_hanzi_display_id_array[len(self.candidate_hanzi) % 8 + 1: 9] = ['' for i in range(0, 8 - len(self.candidate_hanzi_id_array) % 8)]
                        else:
                            self.candidate_hanzi_display[1:9] = self.candidate_hanzi[8 * self.page : 8 * (1 + self.page)]
                            self.candidate_hanzi_display_id_array[1:9] = self.candidate_hanzi_id_array[8 * self.page : 8 * (1 + self.page)]

                else:
                    # self.candidate_hanzi_display = self.candidate_display_reorder_reverse(self.candidate_hanzi_display)
                    # selected_index = self.candidate_display_reorder([0, 2, 4, 6, 8, 16, 18, 28, 30, 36]).index(result_index)
                    selected_index = self.candidate_display_reorder_reverse([0, 2, 4, 6, 8, 16, 18, 28, 30, 36]).index(result_index)

                    if self.candidate_hanzi_display[selected_index] == '':
                        self.candidate_hanzi_display = self.candidate_display_reorder(self.candidate_hanzi_display)
                        self.candidate_hanzi_display_id_array = self.candidate_display_reorder(
                            self.candidate_hanzi_display_id_array)
                        self.fake_strd_producer.send(self.fake_producer_topic, bytes('STRD', encoding='utf-8'))
                        return

                    selected_char = self.candidate_hanzi_display[selected_index]
                    selected_char_id_array = self.candidate_hanzi_display_id_array[selected_index]

                    selected_char_pinyin_array = self.converter.ID2pinyin(selected_char_id_array)

                    tmp = DownListObj(selected_char, 'CH')
                    if tmp.is_punctuation:
                        if len(self.down_list) != 0:
                            if self.down_list[-1].language == 'CH' and self.down_list[-1].is_shengmuyunmu:
                                # if self.down_list[len(self.down_list)-1].is_shengmuyunmu:
                                self.candidate_hanzi_display = self.candidate_display_reorder(
                                    self.candidate_hanzi_display)
                                self.candidate_hanzi_display_id_array = self.candidate_display_reorder(
                                    self.candidate_hanzi_display_id_array)
                                self.fake_strd_producer.send(self.fake_producer_topic, bytes('STRD', encoding='utf-8'))
                                return
                        self.down_list.append(tmp)
                        # self.down_text = ''.join(i.char for i in self.down_list)
                        self.get_down_text()
                    for i, el in enumerate(selected_char_pinyin_array):
                        if i % 2 == 0:
                            ind = min(index for index, item in enumerate(self.down_list) if item.char == el and item.language == 'CH')
                            if i == 0:
                                self.down_list[ind] = tmp # DownListObj(selected_char)
                                if ind < len(self.down_list) - 1:
                                    del self.down_list[ind + 1]
                            else:
                                del self.down_list[ind]
                                if ind < len(self.down_list):
                                    del self.down_list[ind]


                            ind = min(index for index, item in enumerate(self.shengmuyunmu_to_get_candidate_hanzi) if item == el)
                            # del self.shengmuyunmu_to_get_candidate_hanzi[ind]
                            if ind == len(self.shengmuyunmu_to_get_candidate_hanzi) - 1:
                                del self.shengmuyunmu_to_get_candidate_hanzi[ind]
                            else:
                                del self.shengmuyunmu_to_get_candidate_hanzi[ind]
                                del self.shengmuyunmu_to_get_candidate_hanzi[ind]

                    self.candidate_hanzi = [',', '.', ';', ':', "'", '"', '!', '`', '@', '(', ')']
                    self.candidate_hanzi_display = ['上', ',', '.', ';', ':', "'", '"', '!', '`', '下']
                    # [';', ':', "'", '"', '.', '!', ',', '`', '上', '下']
                    self.candidate_hanzi_id_array = ['', '', '', '', '', '', '', '', '', '', '', '']
                    self.candidate_hanzi_display_id_array = ['', '', '', '', '', '', '', '', '', '']
                    self.page = 0
                    self.max_page = 1

                    if len(self.shengmuyunmu_to_get_candidate_hanzi) > 0:
                        idArray = pinyin2ID(self.shengmuyunmu_to_get_candidate_hanzi, self.IDTable)
                        ch = self.converter.getCandidateChar(idArray)
                        self.candidate_hanzi = ch.character
                        self.candidate_hanzi_id_array = ch.idArray
                        if len(self.candidate_hanzi) < 8:
                            self.max_page = 0
                            self.candidate_hanzi_display[1:len(self.candidate_hanzi) + 1] = self.candidate_hanzi[0 : len(self.candidate_hanzi)]
                            for i in range(len(self.candidate_hanzi) + 1, 9):
                                self.candidate_hanzi_display[i] = ''
                            self.candidate_hanzi_display_id_array[1:len(self.candidate_hanzi) + 1] = self.candidate_hanzi_id_array[0 : len(self.candidate_hanzi)]
                        else:
                            self.max_page = int(len(self.candidate_hanzi) / 8 + 1)
                            self.candidate_hanzi_display[1:9] = self.candidate_hanzi[0:8]
                            self.candidate_hanzi_display_id_array[1:9] = self.candidate_hanzi_id_array[0:8]

                    # self.down_text = ''.join(i.char for i in self.down_list)
                    self.get_down_text()
                    if len(self.shengmuyunmu_to_get_candidate_hanzi) % 2 == 0:
                        self.mode = 0
                    else:
                        self.mode = 1

        else: # self.mode == 2
            result_obj = DownListObj(result_char, 'EN')

            if result_obj.is_punctuation:
                self.enter_counter = 0
                if len(self.down_list) != 0:
                    if self.down_list[-1].language == 'CH' and self.down_list[-1].is_shengmuyunmu:
                        # if self.down_list[len(self.down_list)-1].is_shengmuyunmu:
                        self.candidate_hanzi_display = self.candidate_display_reorder(self.candidate_hanzi_display)
                        self.candidate_hanzi_display_id_array = self.candidate_display_reorder(
                            self.candidate_hanzi_display_id_array)
                        self.fake_strd_producer.send(self.fake_producer_topic, bytes('STRD', encoding='utf-8'))
                        return
                self.down_list.append(result_obj)
                # self.down_text = ''.join(i.char for i in self.down_list)
                self.get_down_text()
            elif result_obj.char == '<--':
                self.enter_counter = 0
                if len(self.down_list) != 0:
                    if self.down_list[-1].language == 'EN':
                        self.down_list = self.down_list[0:-1]
                        # self.mode = 0
                    else:
                        if not self.down_list[-1].is_shengmuyunmu:
                            if len(self.down_list[-1].char) > 1:
                                self.down_list[-1].char = self.down_list[-1].char[0:-1]
                            else:
                                self.down_list = self.down_list[0:-1]

                        elif self.down_list[-1].is_shengmu:
                            self.down_list = self.down_list[0:-1]
                            self.shengmuyunmu_to_get_candidate_hanzi = self.shengmuyunmu_to_get_candidate_hanzi[0:-1]
                            self.mode = 0

                        else:
                            self.down_list = self.down_list[0:-1]
                            self.shengmuyunmu_to_get_candidate_hanzi = self.shengmuyunmu_to_get_candidate_hanzi[0:-1]
                            self.mode = 1

                    if len(self.shengmuyunmu_to_get_candidate_hanzi) != 0:
                        idArray = pinyin2ID(self.shengmuyunmu_to_get_candidate_hanzi, self.IDTable)
                        ch = self.converter.getCandidateChar(idArray)
                        self.candidate_hanzi = ch.character
                        self.candidate_hanzi_id_array = ch.idArray
                        if len(self.candidate_hanzi) < 8:
                            self.max_page = 0
                            self.candidate_hanzi_display[1:len(self.candidate_hanzi) + 1] = self.candidate_hanzi[0: len(self.candidate_hanzi)]
                            for i in range(len(self.candidate_hanzi) + 1, 9):
                                self.candidate_hanzi_display[i] = ''
                            self.candidate_hanzi_display_id_array[1:len(self.candidate_hanzi) + 1] = self.candidate_hanzi_id_array[0: len(self.candidate_hanzi)]

                        else:
                            self.max_page = int(len(self.candidate_hanzi) / 8)
                            self.candidate_hanzi_display[1:9] = self.candidate_hanzi[0:8]
                            self.candidate_hanzi_display_id_array[1:9] = self.candidate_hanzi_id_array[0:8]

                    else:
                        self.clear()
                        self.max_page = 0
                        self.candidate_hanzi = []
                        self.candidate_hanzi_display = ['', '', '', '', '', '', '', '', '', '']
                        self.candidate_hanzi_id_array = []
                        self.candidate_hanzi_display_id_array = ['', '', '', '', '', '', '', '', '', '']

                # self.down_text = ''.join(i.char for i in self.down_list)
                self.get_down_text()
            elif result_obj.char == '<-┘':
                if len(self.down_list) == 0:
                    self.candidate_hanzi_display = self.candidate_display_reorder(self.candidate_hanzi_display)
                    self.candidate_hanzi_display_id_array = self.candidate_display_reorder(self.candidate_hanzi_display_id_array)
                    self.fake_strd_producer.send(self.fake_producer_topic, bytes('STRD', encoding='utf-8'))
                    self.enter_counter = 0
                    return

                self.enter_counter += 1
                if self.enter_counter == 1 and (self.down_list[-1].language == 'CH' and self.down_list[-1].is_shengmuyunmu):
                    self.del_shengmuyunmu()
                    self.max_page = 0
                    self.candidate_hanzi = []
                    self.candidate_hanzi_display = ['', '', '', '', '', '', '', '', '', '']
                    self.candidate_hanzi_id_array = []
                    self.candidate_hanzi_display_id_array = ['', '', '', '', '', '', '', '', '', '']
                    self.mode = 0

                elif self.enter_counter == 2:
                    # self.up_text = self.up_text + ''.join(i.char for i in self.down_list)
                    self.up_text = ''.join(i.char for i in self.down_list)
                    self.down_list = []
                    self.down_text = ''
                    self.enter_counter = 0
                    self.speak = 1
                    self.doubleSpellingRecordModel.setTime(int(round(time.time() * 1000)))
                    self.doubleSpellingRecordModel.setContent(self.up_text)
                    msg = self.doubleSpellingRecordModel.serialize()
                    self.persistent_producer.send(self.persistent_topic, msg)

            elif result_obj.char == '切换':
                self.enter_counter = 0
                self.del_shengmuyunmu()
                self.mode = 0

            else:
                self.enter_counter = 0
                self.down_list.append(result_obj)
                # self.down_text = ''.join(i.char for i in self.down_list)
                self.get_down_text()

        self.candidate_hanzi_display = self.candidate_display_reorder(self.candidate_hanzi_display)
        self.candidate_hanzi_display_id_array = self.candidate_display_reorder(self.candidate_hanzi_display_id_array)
        message = 'RSLT^' + str(int(result_index))+'^'+str(self.mode)+'^'+self.up_text+'^'+self.down_text+'_'+'^'+'|'.join(self.candidate_hanzi_display)+'^'+str(self.speak)
        self.exchange_message_management.send_exchange_message(message)



        time.sleep(0.5)
        # return result_obj


    def recongize(self, result_id):
        # 总体识别函数, sendStruct中需要包括
        # perpareLastTime, finishLastTime, alphabetId, nextModelIndex, resultString, candidateSet

        # 补充其他参数
        result_obj = {'prepare_last_time': self.prepare_last_time,
                      'finish_last_time': self.finish_last_time,
                      'alphabet_id': result_id}
        return result_obj


    def create_target_template_set(self, frequency_phase_table):
        # 初始化模板
        frequency_set = frequency_phase_table['FREQUENCY']

        # 模板容量足够大
        sample_count = (
                                   self.experiment_information.max_window_time + self.experiment_information.offset_time + 1) * self.experiment_information.down_frequency_sample
        target_template_set = []
        for i in range(len(frequency_set) - 1, -1, -1):
            test_fres = np.mat(
                (frequency_set[i] * (np.arange(1, self.experiment_information.multiplicate_time + 1, 1))).reshape(
                    self.experiment_information.multiplicate_time, 1, order='F'))
            t = np.mat(np.arange(0, 1 / self.experiment_information.down_frequency_sample * (sample_count),
                                 1 / self.experiment_information.down_frequency_sample))
            target_template_set.insert(0, np.vstack(
                (np.exp(-1j * 2 * np.pi * test_fres * t), np.exp(1j * 2 * np.pi * test_fres * t))))
        return target_template_set

    def switch_mode_ch(self):
        if self.mode == 0:
            self.mode = 1
        else:
            self.mode = 0

    def is_correct_yunmu(self, shengmu, yunmu):
        if self.fre_dict[shengmu][yunmu] == 0:
            return 0
        else:
            return 1

    def candidate_display_reorder(self, list):
        list[8],list[6],list[4],list[0],list[1],list[2],list[3],list[5],list[7],list[9] = list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7],list[8],list[9]
        return list

    def candidate_display_reorder_reverse(self, list):
        list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7],list[8],list[9] = list[8],list[6],list[4],list[0],list[1],list[2],list[3],list[5],list[7],list[9]
        return list

    def del_shengmuyunmu(self):
        j = len(self.down_list) - 1
        for i in range(len(self.down_list) - 1, -1, -1):
            if self.down_list[i].language == 'CH' and self.down_list[i].is_shengmuyunmu:
                j -= 1
                continue
            break
        self.down_list = self.down_list[0: j + 1]

        self.clear()
        # self.down_text = ''.join(i.char for i in self.down_list)
        self.get_down_text()

    def get_down_text(self):
        for j in range(len(self.down_list) - 1, -2, -1):
            if j >= 0 and self.down_list[j].language == 'CH' and self.down_list[j].is_shengmuyunmu:
                continue

            if j != len(self.down_list) - 1:
                self.down_list[j + 1].char = '~' + self.down_list[j + 1].char
                self.down_text = ''.join(i.char for i in self.down_list)
                self.down_list[j + 1].char = self.down_list[j + 1].char[1:]
            else:
                self.down_text = ''.join(i.char for i in self.down_list)
            break

    def count_character_num(self):
        count = 0
        for i in self.down_list:
            count += len(i.char)
        return count






