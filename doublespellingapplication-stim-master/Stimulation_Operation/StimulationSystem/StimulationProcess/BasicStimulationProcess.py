from abc import ABCMeta, abstractmethod

class BasicStimulationProcess:
    def __init__(self):
        self.controller = None

    @abstractmethod
    def initial(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def change(self):
        pass

    @abstractmethod
    def run(self):
        pass

