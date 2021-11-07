from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.CommonModule.ResultTransferModel import ResultTransferModel
import logging

class InitialProcess(BasicStimulationProcess):
    def __init__(self):
        self.w = None
        self.initial_texture = None
        self.target_range = None
        self.base_framework_texture = None
        self.prepare_last_time = None
        self.keyboardCallbackImpl = None
        self.keyList = None
        self.logger = logging.getLogger("DoubleSpellingApplication.InitialProcess")

    def initial(self, controller, view_struct, keyboardCallbackImpl, keyList):
        self.logger.debug("DoubleSpellingApplication.InitialProcess.initial is called.")

        self.controller = controller
        self.prepare_last_time = view_struct['prepare_last_time']
        self.initial_texture = view_struct['initial_texture_set'][0]
        self.base_framework_texture = view_struct['base_framework_texture']
        self.w = view_struct['w']
        self.target_range = view_struct['target_range']
        self.keyboardCallbackImpl = keyboardCallbackImpl
        self.keyList = keyList

        self.logger.debug("DoubleSpellingApplication.InitialProcess.initial returned.")

    def update(self):
        pass

    def change(self):
        result_transfer_model = ResultTransferModel()
        result_transfer_model.prepare_last_time = self.prepare_last_time
        result_transfer_model.next_mode = 0
        result_transfer_model.candidate_char = [';', ':', "'", '"', '.', '!', ',', '`', '上', '下']
        self.controller.current_process = self.controller.prepare_process
        self.controller.current_process.update(result_transfer_model)

    def run(self):
        self.logger.debug("DoubleSpellingApplication.InitialProcess.run is called.")

        self.w.flip()
        self.base_framework_texture.draw()
        self.initial_texture.draw()

        self.w.flip()
        self.logger.debug("DoubleSpellingApplication.InitialProcess.run returned.")