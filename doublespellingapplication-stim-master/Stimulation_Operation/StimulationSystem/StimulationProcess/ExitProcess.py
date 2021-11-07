from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
import logging

class ExitProcess(BasicStimulationProcess):
    def initial(self, controller, view_struct):
        self.view_struct = view_struct
        self.controller = controller
        self.logger = logging.getLogger("DoubleSpellingApplication.ExitProcess")
        pass

    def update(self):
        pass

    def change(self):
        pass

    def run(self):
        self.logger.debug("DoubleSpellingApplication.ExitProcess.run is called.")
        for i in self.controller.prepare_process.candidate_char_draw:
            i.autoDraw = False

        self.controller.finish_process.up_to_draw.autoDraw = False
        self.controller.finish_process.down_to_draw.autoDraw = False

        self.controller.clear()
        self.view_struct['base_framework_texture'].draw()
        self.view_struct['w'].flip(clearBuffer=False)
        self.view_struct['w'].close()
        self.logger.debug("DoubleSpellingApplication.ExitProcess.run returned.")
