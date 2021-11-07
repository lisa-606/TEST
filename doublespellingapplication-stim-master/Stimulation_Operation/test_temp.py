import numpy as np
from OperationSystem.AnalysisProcess.Function.EstimateSTEqualizer import EstimateSTEqualizer
import scipy.signal as signal
import datetime
import scipy.io as scio
from OperationSystem.AnalysisProcess.Function.firfilter_matrix import firfilter_matrix
from OperationSystem.AnalysisProcess.OperatorMethod.MultilayerWindowClassifier import MultilayerWindowClassifier
from OperationSystem.AnalysisProcess.OperatorMethod.MultilayerWindowClassifierParameters import MultilayerWindowClassifierParameters
import scipy.linalg as scl

# def iterate_QR(R, new_data):
#     new_data = np.mat(new_data)
#
#     if R is None:
#         G1_size = 0
#         R = new_data.H
#     else:
#         G1_size = R.shape[0]
#         R = np.vstack((R, new_data.H))
#
#     G,R_new,e = scl.qr(R, mode='economic',pivoting=True)  # !!!!!!!!!!
#     # matlabQR分解会重排矩阵，还原重排结果
#     E = np.identity(R_new.shape[1])
#     E = np.mat(E[:,e])
#     R_new = R_new * E.H
#     if G1_size == 0:
#         G1 = np.zeros((8, 8))  # np.mat(np.identity(self.channels_number))
#     else:
#         G1 = G[0:G1_size, :]
#     G2 = G[G1_size:, :]
#     return R_new, G1, G2

def create_target_template_set(frequency_phase_table):
    max_window_time = 6
    offset_time = 0
    down_frequency_sample = 250
    multiplicate_time = 5


    # 初始化模板
    frequency_set = frequency_phase_table['FREQUENCY']

    # 模板容量足够大
    sample_count = (max_window_time + offset_time + 1) * down_frequency_sample
    target_template_set = []
    for i in range(len(frequency_set) - 1, -1, -1):
        test_fres = np.mat(
            (frequency_set[i] * (np.arange(1, multiplicate_time + 1, 1))).reshape(
                multiplicate_time, 1, order = 'F'))

        t = np.mat(np.arange(0, 1 / down_frequency_sample * (sample_count),
                             1 / down_frequency_sample))
        target_template_set.insert(0,
            np.vstack((np.exp(-1j * 2 * np.pi * test_fres * t), np.exp(1j * 2 * np.pi * test_fres * t))))
    return target_template_set

data_file = 'E:/lqbz/postgraduate/Stimulation_Operation/OperationSystem/ReceiveDataClient/fakeData.mat'
data = scio.loadmat(data_file)
fake_data = data['outData']

total_frequency = np.linspace(8.0, 15.2, 10)
target_table = {'FREQUENCY': total_frequency}
target_template_set = create_target_template_set(target_table)

operator_method = MultilayerWindowClassifier()
multilayer_window_classifier_parameters = MultilayerWindowClassifierParameters()

multilayer_window_classifier_parameters.window_step = 0.12 * 250
multilayer_window_classifier_parameters.max_window_length = 6 * 250
multilayer_window_classifier_parameters.channels_number = 8
multilayer_window_classifier_parameters.offset = 0
multilayer_window_classifier_parameters.equalizer_order = [4, 6]

operator_method.initial(multilayer_window_classifier_parameters)

STEqualizer, Pi = EstimateSTEqualizer(fake_data[0:-1, 0:60], [4, 6])

operator_method.set_spatio_temporal_equalizer(STEqualizer)
operator_method.set_template_set(target_template_set)

operator_method.add_data(fake_data[0:-1, 60:90])

for i in range(0,8):
    operator_method.add_data(fake_data[0:-1, 90+i*30:120+i*30])
#DetectProcess.get_result():
min_detection_window_layer = 8
continuous_detection_window_layer = 8
threshold = 1e-7

log_sum_probability = operator_method.get_stop_values()
result_vector = operator_method.classify()
# print(result_vector)
windows_flag = []
for i in range(0, len(log_sum_probability)):
    windows_flag.append(False)

for i in range(min_detection_window_layer-1, len(log_sum_probability)):
    last_result_vector = result_vector[i - continuous_detection_window_layer : i]

    windows_flag[i] = (log_sum_probability[i] < -np.log(1- threshold)) and not np.any(np.diff(last_result_vector))

stop_flag = np.any(windows_flag)
windows_flag = np.array(windows_flag)
stop_window_index = np.argwhere(windows_flag == True)  # [0, 0]
if stop_flag:
    stop_window_index = stop_window_index[0, 0]
result = result_vector[stop_window_index]

# return stop_flag, result, stop_window_index



# output_data, Zf = firfilter_matrix(STEqualizer, fake_data[0:-1, 60:90], None)
#
# output_data, Zf = firfilter_matrix(STEqualizer, fake_data[0:-1, 90:120], Zf)
#
# R_new, G1, G2 = iterate_QR(None, output_data)
# R_new, G1, G2 = iterate_QR(R_new, output_data)
# print(G2)
# print(output_data)


