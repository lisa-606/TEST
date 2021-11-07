from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.CommonModule.ResultTransferModel import ResultTransferModel
from psychopy import visual, event
import time
import logging

class PrepareProcess(BasicStimulationProcess):
    def __init__(self):
        self.w = None
        self.initial_texture = None
        self.target_range = None
        self.base_framework_texture = None
        self.prepare_last_time = None
        self.keyboardCallbackImpl = None
        self.keyList = None
        self.candidate_char_set = None
        self.candidate_char_draw = None
        self.logger = logging.getLogger("DoubleSpellingApplication.PrepareProcess")

    def initial(self, controller, view_struct, keyboardCallbackImpl, keyList):
        self.logger.debug("DoubleSpellingApplication.PrepareProcess.initial is called.")
        self.keyboardCallbackImpl = keyboardCallbackImpl
        self.keyList = keyList
        self.controller = controller
        self.initial_texture_set = view_struct['initial_texture_set']
        self.initial_texture = self.initial_texture_set[0]
        self.base_framework_texture = view_struct['base_framework_texture']
        self.w = view_struct['w']
        self.target_range = view_struct['target_range']
        self.current_mode = 0
        self.candidate_char_set = [';', ':', "'", '"', '.', '!', ',', '`', '上', '下']
        self.candidate_char_draw = []
        self.logger.debug("DoubleSpellingApplication.PrepareProcess.initial rerturned.")

    def update(self, result_transfer_model):
        self.prepare_last_time = result_transfer_model.prepare_last_time
        self.current_mode = result_transfer_model.next_mode

        if self.current_mode == 0 or self.current_mode == 1:
            self.candidate_char_set = result_transfer_model.candidate_char
        else:
            self.candidate_char_set = ['', '', '', '', '', '', '', '', '', '']

        self.initial_texture = self.initial_texture_set[self.current_mode]

    def change(self, result_transfer_model):
        if self.controller.current_process == self.controller.exit_process:
            return
        else:
            self.controller.current_process = self.controller.stimulate_process
            self.controller.current_process.update(result_transfer_model)

    def run(self):
        self.logger.debug("DoubleSpellingApplication.PrepareProcess.run is called.")

        if len(self.candidate_char_draw) != 0:
            for i in self.candidate_char_draw:
                i.autoDraw = False

        self.get_candidate_char_draw()

        for i in self.candidate_char_draw:
            i.autoDraw = True

        self.initial_texture.draw()
        self.w.flip()

        time.sleep(1)

        result_transfer_model = ResultTransferModel()
        result_transfer_model.next_mode = self.current_mode
        self.change(result_transfer_model)
        self.logger.debug("DoubleSpellingApplication.PrepareProcess.run returned.")

    def get_candidate_char_draw(self):
        self.candidate_char_draw.clear()

        xy_set = []
        for i in range(0, 4):
            y = 903
            x = 750 + 140 * i
            xy_set.append([x, y])

            # y = 177
            # x = 750 + 140 * i
            # xy_set.append([x, y])

        y = 782
        x = 680
        xy_set.append([x, y])

        y = 782
        x = 680 + 140 * 4
        xy_set.append([x, y])

        y = 661
        x = 610
        xy_set.append([x, y])

        y = 661
        x = 610 + 140 * 5
        xy_set.append([x, y])

        y = 540
        x = 540
        xy_set.append([x, y])

        y = 540
        x = 540 + 140 * 6
        xy_set.append([x, y])

        for i in range(0, len(self.candidate_char_set)):
            # self.candidate_char_draw.append(
            #     visual.TextStim(self.w, pos=[int(xy_set[i][0] / 1920*1280 - 640), int(xy_set[i][1] / 1080*1024 - 512)], text=self.candidate_char_set[i],
            #                     color=(0, 0, 0),
            #                     colorSpace='rgb255', units='pix'))
            self.candidate_char_draw.append(
                visual.TextStim(self.w,
                                pos=[int(xy_set[i][0] - 1920 / 2), int(xy_set[i][1] - 1080 / 2)],
                                text=self.candidate_char_set[i],
                                color=(200, 200, 200),
                                colorSpace='rgb255', units='pix', font='Microsoft Yahei UI', bold=True, height=25))

    def check_key_board(self):
        for i in event.getKeys():
            if i in self.keyList:
                # self.w.close()
                # core.quit()
                self.keyboardCallbackImpl.keyPressed(i)
                event.clearEvents()
                return True
                # time.sleep(1)

        return False

