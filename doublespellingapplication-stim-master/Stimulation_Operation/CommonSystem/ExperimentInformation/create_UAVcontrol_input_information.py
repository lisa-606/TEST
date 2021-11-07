from doubleSpellingApplication.Stimulation_Operation.CommonSystem.ExperimentInformation.SchemaProcessInformation import SchemaProcessInformation
import numpy as np
import math


def create_UAVcontrol_input_information():
    model_index = 0

    display_char_set = ['下降','上升','左转','右转','后退','前进','左飞','右飞','降落','起飞']

    uav_command_id = list(range(1,11))

    total_frequency = np.linspace(8.0, 15.2, 10)

    total_phase = [0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi, 0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi, 0*math.pi, 0.5*math.pi]

    schema_process_information = SchemaProcessInformation()
    schema_process_information.target_table = { 'ID':list(range(1,11)),
                                                'UAVCOMMANDID':uav_command_id,
                                                'DISPLAYCHAR': display_char_set,
                                                'FREQUENCY': total_frequency,
                                                'PHASE': total_phase }
    return model_index, schema_process_information
