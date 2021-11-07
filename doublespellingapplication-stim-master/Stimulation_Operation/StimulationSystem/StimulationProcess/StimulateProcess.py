from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from psychopy import visual, core, event
import datetime
import time
import logging

class StimulateProcess(BasicStimulationProcess):
    def __init__(self):
        self.w = None
        self.exchange_message_management = None
        self.stimulate_max_time = None
        self.frame_texture_set = None
        self.target_range = None
        self.trigger_code = None
        self.current_mode = None
        self.up_text = None
        self.down_text = None
        self.keyboardCallbackImpl = None
        self.keyList = None
        self.logger = logging.getLogger("DoubleSpellingApplication.StimulateProcess")

    def initial(self, controller, view_struct, exchange_message_management, keyboardCallbackImpl, keyList):
        self.logger.debug("DoubleSpellingApplication.StimulateProcess.initial is called.")
        self.keyboardCallbackImpl = keyboardCallbackImpl
        self.keyList = keyList
        self.controller = controller
        self.base_framework_texture = view_struct['base_framework_texture']
        self.frame_texture_set = view_struct['frame_texture_set']
        self.w = view_struct['w']
        self.target_range = view_struct['target_range']
        self.exchange_message_management = exchange_message_management
        self.current_mode = 0
        self.logger.debug("DoubleSpellingApplication.StimulateProcess.initial returned.")

    def update(self, result_transfer_model):
        self.current_mode = result_transfer_model.next_mode

    def change(self, result_transfer_model):
        if self.controller.current_process == self.controller.exit_process:
            return
        else:
            self.controller.current_process = self.controller.finish_process
            self.controller.current_process.update(result_transfer_model)

    def run(self):
        self.logger.debug("DoubleSpellingApplication.StimulateProcess.run is called.")
        controller = self.controller
        frame_no = 0

        frames_texture_vector = self.frame_texture_set[self.current_mode]

        message = 'STRD'
        self.exchange_message_management.send_exchange_message(message)
        self.logger.debug('\nStimulateProcess 发送开始异步检测指令，执行时间{}\n'.format(datetime.datetime.now()))
        frame_index = 0
        # time = 0
        while controller.current_process == controller.stimulate_process:
            #print(frame_no)
            #frame_index = frame_no % len(frames_texture_vector)

            frames_texture_vector[frame_index].draw()

            temp = self.w.flip(clearBuffer=False)
            # print(temp - time)
            # time = temp
            # print(self.w.getActualFrameRate())

            #frame_no += 1
            frame_index += 1
            if frame_index == len(frames_texture_vector):
                frame_index = 0

            if frame_no % 120 == 0:
                self.check_key_board()
            # time.sleep(0.1)

        self.logger.debug("DoubleSpellingApplication.StimulateProcess.run returned.")

    def check_key_board(self):
        for i in event.getKeys():
            if i in self.keyList:
                # self.w.close()
                # core.quit()
                self.keyboardCallbackImpl.keyPressed(i)
                event.clearEvents()
                # raise Exception("SSVEPExperiment: UserInterrupt", '用户中断实验')
                #event.clearEvents()
