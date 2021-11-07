from abc import ABCMeta, abstractmethod


class KeyboardCallbackInterface(metaclass=ABCMeta):

    @abstractmethod
    def keyPressed(self, keyName: str):
        pass