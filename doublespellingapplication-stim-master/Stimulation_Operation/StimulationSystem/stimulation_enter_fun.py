from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.StimulationUIParameters import StimulationUIParameters
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.Singleton.SingletonStimulationController import controller_StimulationController
import datetime
import time
from psychopy import visual, core, event
import os


def stimulation_enter_fun(experiment_information,paradigm_config,state_monitor,exchange_message_management):
    message = 'CTNS'
    exchange_message_management.send_exchange_message(message)
    print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(state_monitor.status,
            'CTOK', datetime.datetime.now()))

    while state_monitor.status != 'CTOK':
        time.sleep(0.1)

    message = 'STAR'
    exchange_message_management.send_exchange_message(message)
    print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(state_monitor.status,
            'TROK', datetime.datetime.now()))

    while state_monitor.status != 'TROK':
        time.sleep(0.1)

    experiment_information.experiment_start_time = datetime.datetime.now()
    print(datetime.datetime.now())

    mywin = visual.Window([1920, 1080], monitor="testMonitor", units="pix", fullscr=True, waitBlanking=False,
                          color=(0, 0, 0), colorSpace='rgb255', useFBO = True, allowStencil = True) #  waitBlanking=True,

    relax_text = visual.TextStim(mywin, pos=[0, 0], text='系统初始化，请保持放松\n\n\n运行过程中，按住ESC键可退出实验', color=(255, 255, 255), colorSpace='rgb255', )
    relax_text.draw()
    mywin.flip()

    stimulation_frames_path = paradigm_config.stimulation_frames_path
    stim_target_rect_set = paradigm_config.stim_target_rect_set

    frame_set = []
    initial_frame_set = []
    #stim_target_rect_set = []
    for i in range(0,len(stimulation_frames_path)):
        temp_frame_set = stimulation_frames_path[i][1:len(stimulation_frames_path[i])]
        frame_set.append(temp_frame_set)
        initial_frame_set.append(stimulation_frames_path[i][0])

    stimulation_ui_parameters = StimulationUIParameters()

    target_range = stimulation_ui_parameters.target_range

    base_framework = paradigm_config.background_frame_path
    base_framework_texture = visual.ImageStim(mywin, image=base_framework, pos=[0, 0], size=[1920, 1080], units='pix', flipVert=False)
    initial_texture_set = []
    frame_texture_set = []
    for modelIndexI in range(0,len(frame_set)):
        initial_frame_temp = initial_frame_set[modelIndexI]
        initial_texture_set.append(visual.ImageStim(mywin, image=initial_frame_temp, pos=[0, 0], units='pix'))#, size=[1920, 1080]
        frames_temp = frame_set[modelIndexI]
        frames_texture_vector = []
        for i in range(0, len(frames_temp)):
            frames_texture_vector.append(visual.ImageStim(mywin, image=frames_temp[i], pos=[0, 0], units='pix'))#, size=[1920, 1080], flipVert=False
        frame_texture_set.append(frames_texture_vector)

    view_struct = {'frame_texture_set' : frame_texture_set,
                   'base_framework_texture' : base_framework_texture,
                   'initial_texture_set' : initial_texture_set,
                   'target_range' : target_range,
                   'stim_target_rect_set' : stim_target_rect_set,
                   'w' : mywin,
                   'prepare_last_time' : experiment_information.prepare_last_time,
                   'target_table' : experiment_information.schema_process_information.target_table}

    stimulation_controller = controller_StimulationController
    stimulation_controller.initial(view_struct, exchange_message_management)
    # time.sleep(5)

    prepare_finish_text = visual.TextStim(mywin, pos=[0, 0], text='系统准备完毕，即将开始实验。', color=(255, 255, 255),
                                 colorSpace='rgb255')
    prepare_finish_text.draw()
    mywin.flip()
    time.sleep(0.5)
    print(datetime.datetime.now())
    message = 'STON'
    exchange_message_management.send_exchange_message(message)
    while state_monitor.status != 'TNOK':
        print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(state_monitor.status, 'TNOK', datetime.datetime.now()))
        time.sleep(0.1)

    stimulation_controller.run()
    stimulation_controller.change()

    while True:
        stimulation_controller.run()
        if len(event.getKeys()) > 0:
            break
        event.clearEvents()

    return experiment_information

