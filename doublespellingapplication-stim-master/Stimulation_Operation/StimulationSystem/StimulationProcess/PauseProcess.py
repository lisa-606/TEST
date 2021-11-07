from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
# from psychopy import event

class PauseProcess(BasicStimulationProcess):
    def __init__(self):
        self.exchange_message_management = None
        self.w = None
        self.base_framework_texture = None
        self.candidate_site_rect_set = None
        self.stim_target_rect_set = None
        self.initial_texture = None
        self.finish_last_time = None
        self.target_range = None
        self.keyboardCallbackImpl = None
        self.keyList = None


    def initial(self, controller, view_struct, exchange_message_management, keyboardCallbackImpl, keyList):
        self.keyboardCallbackImpl = keyboardCallbackImpl
        self.keyList = keyList
        self.controller = controller
        self.exchange_message_management = exchange_message_management
        self.initial_texture = view_struct['initial_texture_set'][0]
        self.base_framework_texture = view_struct['base_framework_texture']
        self.w = view_struct['w']
        self.target_range = view_struct['target_range']
        self.stim_target_rect_set = view_struct['stim_target_rect_set']

    def update(self):
        pass

    def change(self):
        self.controller.currenr_process = self.controller.prepare_process

    def run(self):
        self.show_result()
        self.show_pause_frame()

        self.check_key_board()

        self.change()
        self.show_result()
        # self.check_key_board()

    def show_result(self):
        self.base_framework_texture.draw()

    # def check_key_board(self):
    #     for i in event.getKeys():
    #         if i in self.keyList:
    #             # self.w.close()
    #             # core.quit()
    #             # self.keyboardCallbackImpl.keyPressed(i)
    #             raise Exception("SSVEPExperiment: UserInterrupt", '用户中断实验')
    #             # event.clearEvents()

