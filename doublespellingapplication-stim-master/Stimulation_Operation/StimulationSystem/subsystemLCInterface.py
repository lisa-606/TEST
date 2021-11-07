from abc import ABCMeta, abstractmethod
from xml.dom.minidom import Element

from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.keyboardCallbackInterface import KeyboardCallbackInterface


class SubsystemLCInterface(metaclass=ABCMeta):

    @abstractmethod
    def initial(self, keyList: list = None, keyPressedCallback: KeyboardCallbackInterface = None, config: Element = None):
        """

        :param keyList: list<str>，每个元素表征键盘上的一个按键名，刺激子系统需要将该list中的按键绑定到psychopy键盘监听器中，如果绑定失败
        （比如该元素不是按键名）请直接抛出子系统级异常并关闭所有子线程后退出
        :param keyPressedCallback: 请绑定至psychopy键盘监听器中，如果上述按键被按下则调用该回调函数，传入按键名
        :param config: 1.0版本无需关注该参数
        :return:
        """
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
