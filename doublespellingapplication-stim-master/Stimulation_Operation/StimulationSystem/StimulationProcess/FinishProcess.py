from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from psychopy import visual, event
import time
# from psychopy.tools.monitorunittools import posToPix,cm2pix
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.Text2Speak.SpeakerImplement import SpeakerImplement
import logging

class FinishProcess(BasicStimulationProcess):
    def __init__(self):
        self.w = None
        self.stim_target_rect_set = None
        self.initial_texture = None
        self.finish_last_time = None
        self.target_range = None
        self.alphabet_id = None
        #self.speak_controller = None
        self.target_table = None

        self.result_transfer_model = None
        self.up_to_draw = None
        self.down_to_draw = None
        self.candidate_char_set = None
        self.candidate_char_draw = None
        self.keyboardCallbackImpl = None
        self.keyList = None
        self.speaker = None
        self.speak = None
        self.logger = logging.getLogger("DoubleSpellingApplication.FinishProcess")

    def initial(self, controller, view_struct, keyboardCallbackImpl, keyList):
        self.logger.debug("DoubleSpellingApplication.FinishProcess.initial is called.")
        self.keyboardCallbackImpl = keyboardCallbackImpl
        self.keyList = keyList
        self.controller = controller
        self.initial_texture_set = view_struct['initial_texture_set']
        self.initial_texture = self.initial_texture_set[0]
        self.base_framework_texture = view_struct['base_framework_texture']
        self.w = view_struct['w']
        self.target_range = view_struct['target_range']
        self.stim_target_rect_set = view_struct['stim_target_rect_set']
        #self.speak_controller = SpeakController.speak_controller
        self.target_table = view_struct['target_table']
        self.current_mode = 0
        self.up_text = ''
        self.down_text = ''
        # self.up_to_draw = visual.TextStim(self.w, pos=[0, int((451 + 60) / 540 * 512)], text=self.up_text,
        #                                   color=(255, 255, 255),
        #                                   colorSpace='rgb255', units='pix')
        # self.down_to_draw = visual.TextStim(self.w, pos=[0, int((451 + 30) / 540 * 512)], text=self.down_text,
        #                                     color=(255, 255, 255),
        #                                     colorSpace='rgb255', units='pix')
        self.up_to_draw = visual.TextStim(self.w, pos=[0, int(451 + 60)], text=self.up_text,
                                          color=(255, 255, 255),
                                          colorSpace='rgb255', units='pix')
        self.down_to_draw = visual.TextStim(self.w, pos=[0, int(451 + 30)], text=self.down_text,
                                            color=(255, 255, 255),
                                            colorSpace='rgb255', units='pix')
        # self.candidate_char_set = ['一','二','三','四','五','六','七','八','九','十']
        self.candidate_char_draw = []
        # self.get_candidate_char_draw()
        self.speaker = SpeakerImplement(gender='male',rate=150,volume=1)
        self.speak = 0
        self.logger.debug("DoubleSpellingApplication.FinishProcess.initial returned.")

    def update(self, result_transfer_model):
        self.logger.debug("DoubleSpellingApplication.FinishProcess.update is called.")
        self.finish_last_time = result_transfer_model.finish_last_time
        self.alphabet_id = result_transfer_model.alphabet_id
        self.result_transfer_model = result_transfer_model
        self.current_mode = result_transfer_model.next_mode
        self.up_text = result_transfer_model.up_text
        self.down_text = result_transfer_model.down_text
        self.speak = result_transfer_model.speak
        # self.candidate_char_set = result_transfer_model.candidate_char

        self.up_to_draw.autoDraw = False
        self.down_to_draw.autoDraw = False


        for i in self.candidate_char_draw:
            i.autoDraw = False

        self.logger.debug("DoubleSpellingApplication.FinishProcess.update returned.")

    def change(self, result_transfer_model):
        if self.controller.current_process == self.controller.exit_process:
            return
        else:
            self.controller.current_process = self.controller.prepare_process
            self.controller.current_process.update(result_transfer_model)

    def run(self):
        self.logger.debug("DoubleSpellingApplication.FinishProcess.run is called.")

        self.show_result()

        self.initial_texture = self.initial_texture_set[self.current_mode]
        self.change(self.result_transfer_model)
        self.logger.debug("DoubleSpellingApplication.FinishProcess.run returned.")

    def show_result(self):
        self.base_framework_texture.draw()
        self.initial_texture.draw()

        # print(self.up_to_draw)
        # print(self.down_to_draw)

        # self.up_to_draw = visual.TextStim(self.w, pos=[0, int((451+60)/540*512)], text=self.up_text, color=(255, 255, 255),
        #                                     colorSpace='rgb255', units = 'pix',alignText='left',
        #                                     anchorVert='bottom')
        # self.down_to_draw = visual.TextStim(self.w, pos=[0, int((451+30)/540*512)], text=self.down_text, color=(255, 255, 255),
        #                                     colorSpace='rgb255', units = 'pix',alignText='left',
        #                                     anchorVert='bottom')
        self.up_to_draw = visual.TextStim(self.w, pos=[0, int(451 + 60)], text=self.up_text,
                                          color=(255, 255, 255),
                                          colorSpace='rgb255', units='pix', alignText='left',
                                          anchorVert='bottom', height=25)
        self.down_to_draw = visual.TextStim(self.w, pos=[0, int(451 + 30)], text=self.down_text,
                                            color=(255, 255, 255),
                                            colorSpace='rgb255', units='pix', alignText='left',
                                            anchorVert='bottom', height=25)
        # if self.candidate_char_set[6] == '':
        #     for i in self.candidate_char_draw:
        #         i.draw()
        #
        # self.get_candidate_char_draw()
        #
        # for i in self.candidate_char_draw:
        #     i.autoDraw = True
            # i.draw()



        self.up_to_draw.autoDraw = True
        self.down_to_draw.autoDraw = True
        # self.up_to_draw.draw()
        # self.down_to_draw.draw()
        #print(self.alphabet_id)

        if not self.alphabet_id == None:
            stim_target_rect_cell = self.stim_target_rect_set[0]
            result_target = stim_target_rect_cell[self.alphabet_id]

            # frame_rect = visual.Circle(self.w, lineColor=[0,0,255], lineColorSpace='rgb255', pos=(int(result_target.site_point[0]/1920*1280 - 1280/2), int(result_target.site_point[1]/1080*1024 - 1024/2)), size = [70,100], units = 'pix', lineWidth = 5)
            frame_rect = visual.Circle(self.w, lineColor=[0, 0, 255], lineColorSpace='rgb255', pos=(
                int(result_target.site_point[0] - 1920 / 2),
                int(result_target.site_point[1] - 1080 / 2)), size=[100, 100], units='pix', lineWidth=5)
            #frame_rect = visual.Rect(self.w, lineColor=[0, 0, 255], lineColorSpace='rgb255', pos = posToPix(frame_rect), size=(160, 160))

            frame_rect.draw()

        self.w.flip(clearBuffer = False)

        if self.speak == 1:
            self.speaker.speak(self.up_text)
            self.speak = 0
        time.sleep(1)

    def get_candidate_char_draw(self):
        self.candidate_char_draw.clear()

        xy_set = []
        for i in range(0, 4):
            y = 903
            x = 750 + 140 * i
            xy_set.append([x,y])

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
                                pos=[int(xy_set[i][0] - 1920/2), int(xy_set[i][1] - 1080/2)],
                                text=self.candidate_char_set[i],
                                color=(200, 200, 200),
                                colorSpace='rgb255', units='pix',font='Microsoft Yahei UI', bold=True))

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


