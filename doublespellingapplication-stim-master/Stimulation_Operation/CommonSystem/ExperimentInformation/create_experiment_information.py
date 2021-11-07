from doubleSpellingApplication.Stimulation_Operation.CommonSystem.ExperimentInformation.MultilayerWindowClassifierExperimentInformation import MultilayerWindowClassifierExperimentInformation
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.ExperimentInformation.create_doublespelling_input_information import create_doublespelling_input_information
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.ExperimentInformation.PreprocessFilter import PreprocessFilter
import numpy as np
import math
from scipy import signal


def create_experiment_information(user_name, user_folder_path):
    experiment_information = MultilayerWindowClassifierExperimentInformation()
    experiment_information.save_path = user_folder_path + '/' + user_name + '.mat'

    experiment_information.frame_rate = 120

    #experiment_information.stimulation_max_time = 5

    experiment_information.prepare_last_time = 0.5

    experiment_information.finish_last_time = 0.5

    experiment_information.stimulation_frequency_set = np.linspace(8.0, 15.8, 40)

    experiment_information.stimulation_phase_set = [0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                                                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                                                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                                                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                                                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                                                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                                                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                                                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                                                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                                                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi]

    model_index, schema_process_information = create_doublespelling_input_information()

    experiment_information.schema_process_information = schema_process_information

    experiment_information.channel_no = 8

    experiment_information.frequency_sample = 1000

    experiment_information.down_frequency_sample = 250

    experiment_information.multiplicate_time = 5

    experiment_information.window_step_time = 0.12

    experiment_information.max_window_time = 6

    experiment_information.offset_time = 0

    experiment_information.equalizer_order = [4, 6]

    experiment_information.threshold = 1e-7

    experiment_information.min_detection_window_layer = 8

    experiment_information.continuous_detection_window_layer = 8

    experiment_information.equalizer_update_time = 10

    experiment_information.equalizer_estimate_time = 90

    fs = 250.0  # Sample frequency (Hz)
    f0 = 50.0  # Frequency to be removed from signal (Hz)
    Q = 35.0  # Quality factor
    w0 = f0 / (fs / 2)  # Normalized Frequency
    # Design notch filter
    preprocess_filter = PreprocessFilter()
    preprocess_filter.B, preprocess_filter.A = signal.iirnotch(w0, Q)
    experiment_information.preprocess_filter = preprocess_filter
    return experiment_information
