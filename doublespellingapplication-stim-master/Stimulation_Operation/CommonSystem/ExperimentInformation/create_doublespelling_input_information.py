from doubleSpellingApplication.Stimulation_Operation.CommonSystem.ExperimentInformation.SchemaProcessInformation import SchemaProcessInformation
import numpy as np
import math


def create_doublespelling_input_information():
    model_index = 0

    shengmu_display_char_set = ['', '<--', '', 'z', '', 'c', '', 'p', '', 'e',
                                'f', 'ch', 'q', 'zh', 'k', 'w', '', 'r', '', 'o',
                                'm', 'h', 'y', 'sh', 'l', 'x', 't', 'b', '',
                                'a', '', 'n', 'd', 'j', 'g', 's', '',
                                '切换', ' ', '<-┘']

    yunmu_display_char_set = ['', '<--', '', 'ui\nv', '', 'en', '', 'uang\niang', '', 'e',
                              'ue', 'eng', 'ie', 'ang', 'iu', 'ei', '', 'un', '', 'uo\no',
                              'in', 'u', 'ou', 'ong\niong', 'ian', 'uai\ning', 'iao', 'an', '',
                              'a', '', 'uan\ner', 'i', 'ua\nia', 'ai', 'ao', '',
                              '切换', ' ', '<-┘']

    english_display_char_set = ['3', '<--', '4', 'z', '5', 'c', '6', 'p', '2', 'e',
                                'f', 'i', 'q', 'u', 'k', 'w', '7', 'r', '1', 'o',
                                'm', 'h', 'y', 'v', 'l', 'x', 't', 'b', '8',
                                'a', '0', 'n', 'd', 'j', 'g', 's', '9',
                                '切换', ' ', '<-┘']

    doublespeing_command_id = list(range(1,41))

    total_frequency = np.linspace(8.0, 15.8, 40)

    total_phase = [0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi,
                     0*math.pi, 0.5*math.pi, 1*math.pi, 1.5*math.pi]

    shengmu_target_table = { 'ID':doublespeing_command_id,
                            'DOUBLESPELLINGCOMMANDID':doublespeing_command_id,
                            'DISPLAYCHAR': shengmu_display_char_set,
                            'FREQUENCY': total_frequency,
                            'PHASE': total_phase }

    yunmu_target_table = {'ID': doublespeing_command_id,
                           'DOUBLESPELLINGCOMMANDID': doublespeing_command_id,
                           'DISPLAYCHAR': yunmu_display_char_set,
                           'FREQUENCY': total_frequency,
                           'PHASE': total_phase}

    english_target_table = {'ID': doublespeing_command_id,
                            'DOUBLESPELLINGCOMMANDID': doublespeing_command_id,
                            'DISPLAYCHAR': english_display_char_set,
                            'FREQUENCY': total_frequency,
                            'PHASE': total_phase}

    schema_process_information = SchemaProcessInformation()

    schema_process_information.target_table.append(shengmu_target_table)
    schema_process_information.target_table.append(yunmu_target_table)
    schema_process_information.target_table.append(english_target_table)

    return model_index, schema_process_information
