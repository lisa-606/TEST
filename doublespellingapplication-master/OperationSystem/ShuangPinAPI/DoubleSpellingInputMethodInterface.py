

from abc import ABCMeta, abstractmethod


class DoubleSpellingInputMethodInterface(metaclass=ABCMeta):
    """
    this class is an interface of pinyin-> Chinese, the implement of the
    interface is in the "DoubleSpellingInputMethodInterface" class.
    """

    def __init__(self,maxLenCharacter, maxWordNumber):
        # 限定检索的词的中文字符最长长度(default=2)
        self.maxLenCharacter = maxLenCharacter
        # 单次返回最大词组数
        self.maxWordNumber = maxWordNumber

    # 根据当前ID数组返回候选中文字符合集
    # 返回CandidateChinese 类
    @abstractmethod
    def getCandidateChar(self,idArray):
        pass

    # 返回当前ID数组,返回拼音字符串
    @abstractmethod
    def getPinYin(self,idArray):
        pass

    # 根据当前输入ID序号返回下一次备选的id数组

    @abstractmethod
    def getNextIDSet(self,id):
        pass

        # 接口转换函数, 输入string为拼音内容, 可包含多个音节词
        # resultStruct 为返回的结构体,其中包含两个元素, 分别为:
        # resultStruct.word 记录返回多音节词组,
        # resultStruct.character 为返回单音节汉字