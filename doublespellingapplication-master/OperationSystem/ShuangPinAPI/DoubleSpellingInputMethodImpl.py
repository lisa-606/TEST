from typing import List, Union, Any
import os
import numpy as np
import sys
sys.path.append('..')

import pandas as pd
import logging
from doubleSpellingApplication.OperationSystem.ShuangPinAPI.DoubleSpellingInputMethodInterface import DoubleSpellingInputMethodInterface as IPinyin
from doubleSpellingApplication.OperationSystem.ShuangPinAPI.CandidateChinese import Candidate
from doubleSpellingApplication.OperationSystem.ShuangPinAPI.Utils import IDTableLoader, CombinationLoader
from doubleSpellingApplication.OperationSystem.ShuangPinAPI.pinyin2ID import pinyin2ID


class DoubleSpellingInputMethodImpl(IPinyin):
    """
    This class is an implement os DoublePinInputMethod Interface
    """

    def __init__(self, maxLenCharacter, maxWordNumber):
        super().__init__(maxLenCharacter, maxWordNumber)
        __path = os.path.dirname(__file__)
        self.Combination = CombinationLoader(os.path.join(__path, 'Combination.npy'))
        self.dictionary_word = np.load(os.path.join(__path, 'ndictionary_word.npy'), allow_pickle=True).tolist()
        self.IDTable = IDTableLoader(os.path.join(__path, 'IDTable.csv'))
        self.ref_pinyin2ID_yunmu = np.load(os.path.join(__path, 'reference_pinyin2ID_yunmu.npy'),
                                           allow_pickle=True).tolist()
        self.logger = logging.getLogger("DoubleSpellingApplication.DoubleSpellingInputMethodImpl")

    def getCandidateChar(self, idArray):
        """
        根据当前idArray数组返回候选集合
        idarray -> pinyin string -> search -> return Chinese and idarray
        :param idArray: that idArray
        :return:chinese
        """
        candidateChineseSet = Candidate()
        effectIDArrayLen = min(len(idArray), 2 * self.maxLenCharacter)
        idArray = idArray[0:effectIDArrayLen]

        if idArray is not []:
            # 非完整输入
            for i in reversed(range(0, len(idArray))):
                if not (i % 2 == 0 and self.getPinYin(idArray[i:i+1]) in ['a', 'e', 'o']):
                    # 单韵母情况
                    if i % 2 == 0 and i == len(idArray) - 1:
                        yunmuList_idArray = self.getNextIDSet(idArray[i])
                        for k in range(0, len(yunmuList_idArray)):
                            # usedPinyin = self.getSeperatedPinYin(yunmuList_idArray[k:k+1])
                            usedPinyin = self.getSeperatedPinYin(idArray + yunmuList_idArray[k:k+1])
                            if usedPinyin in self.dictionary_word:
                                temp = self.dictionary_word[usedPinyin]
                                # print(temp)
                                for word in temp.split(','):
                                    candidateChineseSet.character.append(word)
                                    candidateChineseSet.idArray.append(idArray + yunmuList_idArray[k:k+1])



                    else:
                        usedPinyin = self.getSeperatedPinYin(idArray[0:i + 1])
                        # print(usedPinyin)
                        if usedPinyin in self.dictionary_word:
                            temp = self.dictionary_word[usedPinyin]
                            for word in temp.split(','):
                                candidateChineseSet.character.append(word)
                                # for slt in word.split(','):
                                candidateChineseSet.idArray.append(idArray[0:i + 1])

            return candidateChineseSet

    def getPinYin(self, idArray):
        """
        return the pinyin string by the idArray
        :param idArray: the pinyin ID Array
        :return: a pinyin string
        """
        if len(idArray) != 0:
            if idArray[0] < 27:
                pinYinString = ''
                temp = ''  # 前一个
                for i, k in enumerate(idArray):
                    temp1 = self.IDTable[idArray[i] - 1][2]
                    temp2 = self.IDTable[idArray[i] - 1][3]
                    if type(temp2) is not float:  # 在pandas中,nan的数据类型为float,用此办法检测空
                        if len(temp) != 0:
                            if (temp2 in self.Combination[temp] and
                                    temp1 not in self.Combination[temp]):
                                temp1 = temp2
                    if idArray[0] > 26 and temp in ['a', 'e', 'o']:
                        temp1 = temp1[1:]
                    pinYinString = pinYinString + temp1
                    temp = temp1
                return pinYinString
            else:
                __pinyinString = self.getPinYin(idArray[1:])
                pinyinString = self.IDTable[idArray[0] - 1][2] + __pinyinString
                self.logger.error("输入异常,声母丢失", exc_info=True)
                return pinyinString
        else:
            return ""

    def getNextIDSet(self, id) -> Union[object, Any]:
        """
        根据当前输入ID返回下一次备选的id数组(id->拼音->韵母串->idArray)
        :param id: 当前输入ID
        :return: idArray
        """
        if id < 27:
            shengmu = self.IDTable[id - 1, 2]
            # shengmu = self.IDTable[id-2,2]
            yunmulist = self.Combination[shengmu]
            idArray = self.pinyin2ID(yunmulist)
            return idArray
        else:
            idArray = np.linspace(1, 26, 26, dtype=int).tolist()
            return idArray

    def pinyin2ID(self, pinYin):
        """
        输入为韵母,返回韵母对饮拼音list
        :param pinYin:yunmu list
        :return:yunmu id list
        """
        idArray = []
        for py in pinYin:
            idArray.append(self.ref_pinyin2ID_yunmu[py])
        return idArray

    def ID2pinyin(self, ID):
        """
        返回声母+韵母
        :param ID: 反正是个什么ID
        :return:返回拼音, 针对声母+韵母
        """
        out = []
        for id in ID:
            index = np.where(self.IDTable[0:52, 0] == id)
            # if np.isnan(self.IDTable[index[0].tolist()[0], 3]):
            if not isinstance(self.IDTable[index[0].tolist()[0], 3], str):
                out.append(self.IDTable[index, 2][0][0])
            else:
                out.append(self.IDTable[index[0].tolist()[0], 2] + '\n' + self.IDTable[index[0].tolist()[0], 3])

        return out

    def getSeperatedPinYin(self, idArray):
        """
        # TODO : cannot return right pinyin
        return the pinyin string by the idArray
        :param idArray: the pinyin ID Array
        :return: a pinyin string(seperated)
        """
        if len(idArray) != 0:
            pinYinString = ''
            if idArray[0] < 27:
                temp = ''  # 前一个
                for i, k in enumerate(idArray):
                    temp1 = self.IDTable[idArray[i] - 1][2]
                    temp2 = self.IDTable[idArray[i] - 1][3]
                    if type(temp2) is not float:  # 在pandas中,nan的数据类型为float,用此办法检测空
                        if len(temp) != 0:
                            if (temp2 in self.Combination[temp] and
                                    temp1 not in self.Combination[temp]):
                                temp1 = temp2
                    if idArray[i] > 26 and temp in ['a', 'e', 'o']:
                        temp1 = temp1[1:]
                    pinYinString = pinYinString + temp1
                    if i % 2 == 1:
                        pinYinString += ','
                    temp = temp1

            else:
                __pinyinString = self.getPinYin(idArray[1:])
                pinyinString = self.IDTable[idArray[0] - 1][2] + __pinyinString
                self.logger.error("输入异常,声母丢失", exc_info=True)
            # if pinyinString is not []:
            if pinYinString[-1] == ',':
                return pinYinString[:-1]
            else:
                return pinYinString
        else:
            return ""


if __name__ == '__main__':
    converter = DoubleSpellingInputMethodImpl(2, 5)
    IDTable = IDTableLoader(r'IDTable.csv')
    idArray = pinyin2ID(['e','e'], IDTable)
    # print(idArray)
    ch = converter.getCandidateChar(idArray)
    print(ch.character)
    print(ch.idArray)

    print(converter.ID2pinyin(ch.idArray[0]))
    # print(ch)
    # print(converter.Combination)
