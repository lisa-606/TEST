from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.StimulationUIParameters import StimulationUIParameters
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.BackgroundFrame import BackgroubdFrame
import matplotlib.pyplot as plt
import os


class StimulationUIFactory:
    def __init__(self):
        self.stimulation_frames_factory_list = None
        self.stimulation_ui_parameters = None

    def initial(self, factory):
        self.stimulation_frames_factory_list = factory
        self.stimulation_ui_parameters = StimulationUIParameters()

        for i in range(0, len(self.stimulation_frames_factory_list)):
            self.stimulation_frames_factory_list[i].initial(self.stimulation_ui_parameters)

    def get_background_frame(self):
        '''
        #background_frame = BackgroubdFrame()
        #print(os.getcwd())
        #background_frame.base_framework = plt.imread(self.stimulation_ui_parameters.base_framework_file)
        #return background_frame
        '''
        return self.stimulation_ui_parameters.base_framework_file

    def get_stimulation_frame(self, target_table):
        stimulation_frames = []
        for method_index in range(0, len(self.stimulation_frames_factory_list)):
            stimulation_frames.append(self.stimulation_frames_factory_list[method_index].get_frames(target_table[method_index]))
        return stimulation_frames
