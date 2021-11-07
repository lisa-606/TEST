import sys
sys.path.append('..')
sys.path.append(r'..\CommonSystem\MessageReceiver')

from doubleSpellingApplication.Stimulation_Operation.CommonSystem.ExperimentInformation.create_experiment_information import create_experiment_information
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StateMonitor import StateMonitor
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationExchangeMessageOperator import StimulationExchangeMessageOperator
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.Singleton.SingletonStimulationController import controller_StimulationController
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.ExchangeMessageManagement import ExchangeMessageManagement
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.MessageReceiver.EventManager import EventManager
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.stimulation_enter_fun import stimulation_enter_fun
import os
import pickle
import datetime
import time


folder_path = os.getcwd()
paradigm_name = 'DoubleSpelling'

if not os.path.exists(folder_path+'/stimulationInformationFolder'):
    os.makedirs(folder_path+'/stimulationInformationFolder')

if not os.path.exists(folder_path+'/stimulationInformationFolder'+'/'+paradigm_name):
    os.makedirs(folder_path+'/stimulationInformationFolder'+'/'+paradigm_name)

paradigm_folder_path = folder_path+'/stimulationInformationFolder'+'/'+paradigm_name

experiment_information = create_experiment_information(paradigm_name, paradigm_folder_path)

a_file = open(paradigm_folder_path + '/' + paradigm_name + '_paradigm_config', 'rb')
paradigm_config = pickle.load(a_file)

state_monitor = StateMonitor()
state_monitor.result_string = '>>'
state_monitor.status = 'INIT'

stimulation_exchange_message_operator = StimulationExchangeMessageOperator()
stimulation_exchange_message_operator.experiment_information = experiment_information
stimulation_exchange_message_operator.state_monitor = state_monitor
stimulation_exchange_message_operator.controller =controller_StimulationController
#event_manager = EventManager()
#exchange_message_operator = StimulationExchangeMessageOperator()
topic_stim_receive = 'ope_to_stim'
topic_stim_send = 'stim_to_ope'
exchange_message_management =ExchangeMessageManagement(stimulation_exchange_message_operator, topic_receive = topic_stim_receive, topic_send=topic_stim_send)
exchange_message_management.start()

experimentInformation = stimulation_enter_fun(experiment_information, paradigm_config, state_monitor, exchange_message_management)

message = 'STOP'
exchange_message_management.send_exchange_message(message)
while state_monitor.status != 'PROK':
    print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(state_monitor.status, 'PROK', datetime.datetime.now()))
    time.sleep(0.1)

message = 'DCNS'
exchange_message_management.send_exchange_message(message)
while state_monitor.status != 'DCOK':
    print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(state_monitor.status, 'DCOK', datetime.datetime.now()))
    time.sleep(0.1)

message = 'CSAL'
exchange_message_management.send_exchange_message(message)
while state_monitor.status != 'CAOK':
    print('当前监视器状态{0},等待监视器状态改变为{1},{2}\n'.format(state_monitor.status, 'CAOK', datetime.datetime.now()))
    time.sleep(0.1)

#message = ToOperationSendingExchangeMessage.ExitProgram;
#exchangeMessageManagement.sendExchangeMessage(message);

exchange_message_management.stop()



