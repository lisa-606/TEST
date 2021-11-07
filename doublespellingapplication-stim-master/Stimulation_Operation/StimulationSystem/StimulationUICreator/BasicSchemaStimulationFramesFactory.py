from abc import ABCMeta, abstractmethod


class BasicSchemaStimulationFramesFactory:
    def __init__(self):
        self.stimulation_ui_parameters = None

    @abstractmethod
    def get_frames(self, alpha_table):
        pass

    def initial(self, stimulation_ui_parameters):
        self.stimulation_ui_parameters = stimulation_ui_parameters
