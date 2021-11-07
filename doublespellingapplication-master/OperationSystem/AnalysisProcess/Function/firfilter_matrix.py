import scipy.signal as signal
import numpy as np
from doubleSpellingApplication.OperationSystem.AnalysisProcess.Function.signaltools import lfilter


def firfilter_matrix(filter_cell_matrix, input_data, Zi=None):
    Mo, Mi = filter_cell_matrix.shape[0:2]

    if Mi != input_data.shape[0]:
        raise Exception('error([输入数据与线性系统输入维度不同，线性相位系统维度:', Mi, '输入数据维度', input_data.shape[0],']')
        # print('error([输入数据与线性系统输入维度不同，线性相位系统维度:', Mi, '输入数据维度', input_data.shape[0],']')

    # tempData = zeros(Mo, Mi, size(inputData, 2));
    temp_data = np.array(np.zeros((Mo, Mi, input_data.shape[1])),dtype=complex)

    Zf = np.array(np.zeros((Mo, Mi, filter_cell_matrix.shape[2]-1)),dtype=complex)
    output_data = np.array(np.zeros((Mo, input_data.shape[1])),dtype=complex)

    # for i in range(Mo-1, -1, -1):
    #     if Zi is not None:
    #
    #         temp_data[i, :, :], Zf_temp = lfilter(filter_cell_matrix[i, :, :], np.array([1]), input_data[:,:], zi=Zi[i, :],axis=0)
    #     else:
    #         # Zf_temp = signal.lfilter_zi(filter_cell_matrix[i, j, :], np.array([1]))
    #         t, Zf_temp = lfilter(filter_cell_matrix[i, :, :], np.array([1]), input_data[:,:],axis=0)  #zi= np.ones((filter_cell_matrix.shape[2]-1,))
    #         # Zf_temp = signal.lfiltic(filter_cell_matrix[i, j, :], np.array([1]), t)
    #
    #         temp_data[i, :, :]=t
    #
    #     Zf[i, :, :] = Zf_temp
    #
    #     # output_data[i,:] = sum(cat(1, tempData{i,:}), 1).'
    #     output_data[i, :] = np.vstack((temp_data[i,:])).sum(0).T


    for i in range(Mo-1, -1, -1):
        for j in range(Mi-1, -1, -1):
            if Zi is not None:

                temp_data[i, j, :], Zf_temp = lfilter(filter_cell_matrix[i, j, :], np.array([1]), input_data[j,:], zi=Zi[i, j])
            else:
                # Zf_temp = signal.lfilter_zi(filter_cell_matrix[i, j, :], np.array([1]))
                t, Zf_temp = lfilter(filter_cell_matrix[i, j, :], np.array([1]), input_data[j,:])  #zi= np.ones((filter_cell_matrix.shape[2]-1,))
                # Zf_temp = signal.lfiltic(filter_cell_matrix[i, j, :], np.array([1]), t)

                temp_data[i, j, :]=t

            Zf[i, j, :] = Zf_temp

        # output_data[i,:] = sum(cat(1, tempData{i,:}), 1).'
        output_data[i, :] = np.vstack((temp_data[i,:])).sum(0).T
    return output_data, Zf