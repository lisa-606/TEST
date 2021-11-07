from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.InitialProcess import InitialProcess
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.PrePareProcess import PrepareProcess
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.PauseProcess import PauseProcess
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.StimulateProcess import StimulateProcess
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.FinishProcess import FinishProcess
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.ExitProcess import ExitProcess
import datetime
import logging

class StimulationController:
    def __init__(self):
        self.initial_process = None
        self.prepare_process = None
        self.stimulate_process = None
        self.finish_process = None
        #self.pause_process = None
        self.current_process = None
        #self.over_flag = None
        self.logger = logging.getLogger("DoubleSpellingApplication.StimulationController")

    def initial(self, view_struct, exchange_message_management, keyboardCallbackImpl, keyList):
        self.logger.debug("DoubleSpellingApplication.StimulationController.initiall is called.")

        self.initial_process = InitialProcess()
        self.initial_process.initial(self, view_struct, keyboardCallbackImpl, keyList)

        self.prepare_process = PrepareProcess()
        self.prepare_process.initial(self, view_struct, keyboardCallbackImpl, keyList)

        self.stimulate_process = StimulateProcess()
        self.stimulate_process.initial(self, view_struct, exchange_message_management, keyboardCallbackImpl, keyList)

        self.finish_process = FinishProcess()
        self.finish_process.initial(self, view_struct, keyboardCallbackImpl, keyList)

        self.exit_process = ExitProcess()
        self.exit_process.initial(self, view_struct)


        self.current_process = self.initial_process
        self.logger.debug("DoubleSpellingApplication.StimulationController.initiall returned.")


    def change(self, result_transfer_model = None):
        if result_transfer_model == None:
            self.current_process.change()
        else:
            self.current_process.change(result_transfer_model)

    def run(self):
        self.logger.debug("DoubleSpellingApplication.StimulationController.run is called.")
        self.logger.debug('\n开始进入{0}呈现阶段，执行时间{1}\n'.format(self.__class__.__name__, datetime.datetime.now()))
        self.current_process.run()
        self.logger.debug("DoubleSpellingApplication.StimulationController.run returned.")

    def clear(self):
        self.initial_process = None
        self.prepare_process = None
        self.stimulate_process = None
        self.finish_process = None
        self.current_process = None