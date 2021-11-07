from doubleSpellingApplication.Stimulation_Operation.CommonSystem.ExperimentInformation.create_experiment_information import create_experiment_information
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StateMonitor import StateMonitor
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationExchangeMessageOperator import StimulationExchangeMessageOperator
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.ExchangeMessageManagement import ExchangeMessageManagement
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.EventManager import EventManager
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.StimulationUIParameters import StimulationUIParameters
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationProcess.StimulationController import StimulationController
# from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.subsystemLCInterface import SubsystemLCInterface
from interfaces.subsystemLCInterface import SubsystemLCInterface

from psychopy import visual, core, event
import os
import pickle
import datetime
import time
from logging.handlers import TimedRotatingFileHandler
import logging
import gc


class DoubleSpellingStimController(SubsystemLCInterface):

    # view_struct = None
    # mywin = None

    def __init__(self):
        self.experiment_information = None
        self.paradigm_config = None
        self.state_monitor = None
        self.stimulation_exchange_message_operator = None
        self.exchange_message_management = None
        self.stimulation_ui_parameters = None
        self.stop_flag = False
        self.w = None

        self.logger = logging.getLogger('DoubleSpellingApplication')
        self.logger.setLevel(logging.DEBUG)
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        father_path = os.path.join(os.path.dirname(__file__), os.path.pardir)
        log_file_handler = TimedRotatingFileHandler(filename=fr'{father_path}/dslogs/DoubleSpellingApplication',
                                                    when="D", interval=1,
                                                    backupCount=30, encoding='utf-8')

        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        log_file_handler.setFormatter(formatter)
        self.logger.addHandler(log_file_handler)

    def initial(self, keyList = None, keyPressedCallback = None,  config = None):
        self.logger.debug("DoubleSpellingStimController.initial is called.")
        keyboardCallbackImpl = keyPressedCallback
        self.experiment_information = None
        self.paradigm_config = None
        self.state_monitor = None
        self.stimulation_exchange_message_operator = None
        self.exchange_message_management = None
        self.stimulation_ui_parameters = None
        self.stop_flag = False
        self.w = None
        try:
            # folder_path = os.getcwd()
            # if DoubleSpellingStimController.mywin == None:
            mywin = visual.Window([1920, 1080], monitor="testMonitor", units="pix",
                                                               fullscr=True, waitBlanking=False,
                                                               color=(0, 0, 0), colorSpace='rgb255', pos=(0, 0))  # waitBlanking=True,, useFBO=True,allowStencil=True
            self.w = mywin
            relax_text = visual.TextStim(mywin, pos=[-150, 0], text=u'文字输入应用加载中，请保持放松',
                                         # \n\n\n运行过程中，按住ESC键可退出实验
                                         color=(255, 255, 255), colorSpace='rgb255', height=50)
            relax_text.draw()
            mywin.flip()

            folder_path = os.path.dirname(__file__)
            paradigm_name = 'DoubleSpelling'

            if not os.path.exists(folder_path + '/stimulationInformationFolder'):
                os.makedirs(folder_path + '/stimulationInformationFolder')

            if not os.path.exists(folder_path + '/stimulationInformationFolder' + '/' + paradigm_name):
                os.makedirs(folder_path + '/stimulationInformationFolder' + '/' + paradigm_name)

            paradigm_folder_path = folder_path + '/stimulationInformationFolder' + '/' + paradigm_name

            self.experiment_information = create_experiment_information(paradigm_name, paradigm_folder_path)

            a_file = open(paradigm_folder_path + '/' + paradigm_name + '_paradigm_config', 'rb')
            self.paradigm_config = pickle.load(a_file)

            self.state_monitor = StateMonitor()
            self.state_monitor.result_string = '>>'
            self.state_monitor.status = 'INIT'

            self.stimulation_exchange_message_operator = StimulationExchangeMessageOperator()
            self.stimulation_exchange_message_operator.experiment_information = self.experiment_information
            self.stimulation_exchange_message_operator.state_monitor = self.state_monitor

            topic_stim_receive = 'ope_to_stim_suyan'
            topic_stim_send = 'stim_to_ope_suyan'
            self.exchange_message_management = ExchangeMessageManagement(self.stimulation_exchange_message_operator,
                                                                    topic_receive=topic_stim_receive,
                                                                    topic_send=topic_stim_send)
            self.exchange_message_management.start()


            self.logger.debug('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(self.state_monitor.status,
                                                          'CTOK', datetime.datetime.now()))

            while self.state_monitor.status != 'CTOK':
                message = 'CTNS'
                self.exchange_message_management.send_exchange_message(message)
                time.sleep(0.1)

            message = 'STAR'
            self.exchange_message_management.send_exchange_message(message)
            self.logger.debug('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(self.state_monitor.status,
                                                          'TROK', datetime.datetime.now()))

            while self.state_monitor.status != 'TROK':
                time.sleep(0.1)

            self.experiment_information.experiment_start_time = datetime.datetime.now()

            # if DoubleSpellingStimController.view_struct == None:

            stimulation_frames_path = self.paradigm_config.stimulation_frames_path
            stim_target_rect_set = self.paradigm_config.stim_target_rect_set

            frame_set = []
            initial_frame_set = []

            for i in range(0, len(stimulation_frames_path)):
                temp_frame_set = stimulation_frames_path[i][1:len(stimulation_frames_path[i])]
                frame_set.append(temp_frame_set)
                initial_frame_set.append(stimulation_frames_path[i][0])

            self.stimulation_ui_parameters = StimulationUIParameters()

            target_range = self.stimulation_ui_parameters.target_range

            base_framework = self.paradigm_config.background_frame_path
            base_framework_texture = visual.ImageStim(mywin, image=base_framework, pos=[0, 0], size=[1920, 1080],
                                                      units='pix', flipVert=False)
            initial_texture_set = []
            frame_texture_set = []
            for modelIndexI in range(0, len(frame_set)):
                initial_frame_temp = initial_frame_set[modelIndexI]
                initial_texture_set.append(
                    visual.ImageStim(mywin, image=initial_frame_temp, pos=[0, 0], units='pix'))  # , size=[1920, 1080]
                frames_temp = frame_set[modelIndexI]
                frames_texture_vector = []
                for i in range(0, len(frames_temp)):
                    frames_texture_vector.append(visual.ImageStim(mywin, image=frames_temp[i], pos=[0, 0],
                                                                  units='pix'))  # , size=[1920, 1080], flipVert=False
                frame_texture_set.append(frames_texture_vector)

            view_struct = {'frame_texture_set': frame_texture_set,
                           'base_framework_texture': base_framework_texture,
                           'initial_texture_set': initial_texture_set,
                           'target_range': target_range,
                           'stim_target_rect_set': stim_target_rect_set,
                           'w': mywin,
                           'prepare_last_time': self.experiment_information.prepare_last_time,
                           'target_table': self.experiment_information.schema_process_information.target_table}

            self.stimulation_controller = StimulationController()
            self.stimulation_controller.initial(view_struct, self.exchange_message_management, keyboardCallbackImpl, keyList)
            self.stimulation_exchange_message_operator.controller = self.stimulation_controller
            # time.sleep(5)

            prepare_finish_text = visual.TextStim(mywin, pos=[-230, 0], text=u'系统初始化完毕，即将开始采集背景脑电', color=(255, 255, 255),
                                                  colorSpace='rgb255', height=50)
            prepare_finish_text.draw()
            mywin.flip()
            time.sleep(1)
            self.logger.debug("DoubleSpellingStimController.initial returned.")
        except Exception as e:
            self.logger.fatal(e, exc_info=True)
            self.stop()
            raise e


    def start(self):
        try:
            self.logger.info("DoubleSpellingStimController.start is called")
            message = 'STON'
            self.exchange_message_management.send_exchange_message(message)
            self.logger.debug('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(self.state_monitor.status, 'TNOK', datetime.datetime.now()))

            relax_text = visual.TextStim(self.w, pos=[-300, 0], text=u'背景脑电采集中，请保持放松，应用即将就绪',
                                         # \n\n\n运行过程中，按住ESC键可退出实验
                                         color=(255, 255, 255), colorSpace='rgb255', height=50)
            relax_text.draw()
            self.w.flip()

            while self.state_monitor.status != 'TNOK':
                time.sleep(0.1)

            self.stimulation_controller.run()
            self.stimulation_controller.change()

            while self.stimulation_controller.current_process != self.stimulation_controller.exit_process:
                self.stimulation_controller.run()
                # if len(event.getKeys()) > 0:
                #     break
                # event.clearEvents()
            self.stimulation_controller.run()
            self.logger.info("DoubleSpellingStimController.start returned")
            gc.collect()

        except Exception as e:
            self.logger.fatal(e, exc_info=True)
            self.stop()
            raise e


    def stop(self):
        self.logger.debug('DoubleSpellingStimController.stop is called')
        self.exchange_message_management.stop()
        self.stimulation_controller.current_process = self.stimulation_controller.exit_process
        self.stop_flag = True
        self.logger.debug('DoubleSpellingStimController.stop returned')


if __name__ == '__main__':
    controller = DoubleSpellingStimController()
    # stop_thread = Thread(target=controller.stop,) #args=(self.message_queue,)

    controller.initial(keyList = ['escape'])
    time.sleep(5)

    # stop_thread.start()

    controller.start()



