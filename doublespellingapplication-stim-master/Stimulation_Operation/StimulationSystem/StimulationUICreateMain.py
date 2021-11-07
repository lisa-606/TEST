from doubleSpellingApplication.Stimulation_Operation.CommonSystem.ExperimentInformation.create_experiment_information import create_experiment_information
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.Singleton.SingletonStimulationUIFactory import factory_StimulationUIFactory
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.Singleton.SingletonSchemaStimulationFramesFactory import factory_SchemaStimulationFramesFactory
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.Singleton.SingletonShengmuFramesFactory import factory_ShengmuFramesFactory
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.Singleton.SingletonYunmuFramesFactory import factory_YunmuFramesFactory
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.StimulationUICreator.Singleton.SingletonEnglishFramesFactory import factory_EnglishFramesFactory
from doubleSpellingApplication.Stimulation_Operation.StimulationSystem.ParadigmConfig.ParadigmConfig import ParadigmConfig
import matplotlib.pyplot as plt
import datetime
import  os
import pickle


# folder_path = os.getcwd()
folder_path = os.path.dirname(__file__)
paradigm_name = 'DoubleSpelling'

if not os.path.exists(folder_path+'/stimulationInformationFolder'):
    os.makedirs(folder_path+'/stimulationInformationFolder')

if not os.path.exists(folder_path+'/stimulationInformationFolder'+'/'+paradigm_name):
    os.makedirs(folder_path+'/stimulationInformationFolder'+'/'+paradigm_name)

paradigm_folder_path = folder_path+'/stimulationInformationFolder'+'/'+paradigm_name

experiment_information = create_experiment_information(paradigm_name, paradigm_folder_path)

factory = factory_StimulationUIFactory

frames_factory_list = []

frames_factory_list.append(factory_ShengmuFramesFactory)
frames_factory_list.append(factory_YunmuFramesFactory)
frames_factory_list.append(factory_EnglishFramesFactory)

factory.initial(frames_factory_list)

background_frame = factory.get_background_frame()

stimulation_frames = factory.get_stimulation_frame(experiment_information.schema_process_information.target_table)

paradigm_config = ParadigmConfig()
paradigm_config.paradigm_name = paradigm_name
paradigm_config.save_time = datetime.datetime.now()
paradigm_config.background_frame_path= background_frame

#paradigm_config.stimulation_frames_path = []
#print(len(stimulation_frames))

for num in range(0, len(stimulation_frames)):
    frames_temp = []
    path = folder_path + '/stimulationInformationFolder' + '/' + paradigm_name + '/' +str(num)
    if not os.path.exists(path):
        os.makedirs(path)
    plt.imsave(path + '/initial_frame.png', stimulation_frames[num].initial_frame)
    # plt.savefig(path + '/initial_frame.png', stimulation_frames[num].initial_frame)
    frames_temp.append(path + '/initial_frame.png')
    for frame in range(0, len(stimulation_frames[num].frame_set)):
        frames_temp.append(path + '/' + str(frame) + '.png')
        # plt.imsave(path + '/' + str(frame) + '.png', stimulation_frames[num].frame_set[frame])
        plt.imsave(path + '/' + str(frame) + '.png', stimulation_frames[num].frame_set[frame])

    paradigm_config.stimulation_frames_path.append(frames_temp)
    paradigm_config.stim_target_rect_set.append(stimulation_frames[num].stim_target_rect_set)

a_file = open(paradigm_folder_path + '/' + paradigm_name + '_paradigm_config', 'wb')
pickle.dump(paradigm_config, a_file)
a_file.close()
''''''
a_file = open(paradigm_folder_path + '/' + paradigm_name + '_paradigm_config', 'rb')
output = pickle.load(a_file)
print(output)

