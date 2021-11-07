import numpy as np
import scipy.linalg as scl
import datetime
import time
import logging
from doubleSpellingApplication.OperationSystem.AnalysisProcess.Function.EstimateSTEqualizer import EstimateSTEqualizer
from doubleSpellingApplication.OperationSystem.AnalysisProcess.Function.firfilter_matrix import firfilter_matrix



class MultilayerWindowClassifier:
    def __init__(self):
        self.channels_number = None
        self.window_step = None
        self.max_window_length = None
        self.offset = None
        self.equalizer_order = None
        self.template_set = None
        self.template_set_p_cell = None
        self.template_G1 = None
        self.template_G2 = None
        self.spatio_temporal_equalizer = None
        self.QxQy_inner_product_cell = None
        self.current_max_window_index = None
        self.reach_full_window_flag = None
        self.equalized_data_zf = None
        self.equalized_data_R = None

        self.logger = logging.getLogger("DoubleSpellingApplication.MultilayerWindowClassifier")

    def initial(self, multilayer_window_classifier_parameters):
        self.logger.debug("MultilayerWindowClassifier.initial is called.")

        self.window_step = multilayer_window_classifier_parameters.window_step

        self.max_window_length = multilayer_window_classifier_parameters.max_window_length

        self.channels_number = multilayer_window_classifier_parameters.channels_number

        self.offset = multilayer_window_classifier_parameters.offset

        self.equalizer_order = multilayer_window_classifier_parameters.equalizer_order

        self.reach_full_window_flag = False

        # 初始化内积组合

        # self.XX_EnergyVector = zeros(1, (obj.maxWindowLength + obj.offset) / obj.windowStep);

        # self.XY_InnerProductCell = cell(length(obj.templateSet), (obj.maxWindowLength + obj.offset) / obj.windowStep);

        # self.QxQy_inner_product_cell = np.array(np.zeros((10, int((self.max_window_length + self.offset) / self.window_step), self.channels_number, int(self.window_step))))
        self.QxQy_inner_product_cell = np.empty((40, int((self.max_window_length + self.offset) / self.window_step)), dtype=object)
        for i in range(0, self.QxQy_inner_product_cell.shape[0]):
            for j in range(0, self.QxQy_inner_product_cell.shape[1]):
                self.QxQy_inner_product_cell[i,j] = np.mat(np.zeros((self.channels_number,self.channels_number)))

        # len(self.template_set)
        self.current_max_window_index = 1

        # 初始化均衡数据参数
        self.equalized_data_zf = None

        self.equalized_data_R = None

    def update_equalizer(self,noise_data):
        self.spatio_temporal_equalizer = EstimateSTEqualizer(noise_data,self.equalizer_order )


    def add_data(self, new_data):
        if new_data.shape[1] != self.window_step:
            self.logger.error('[输入数据长度与预定窗长不匹配。 预定窗长', str(self.window_step),' 实际输入数据长度',str(new_data.shape[1]),']')
            raise Exception('error([输入数据长度与预定窗长不匹配。 预定窗长', str(self.window_step),' 实际输入数据长度',str(new_data.shape[1]),']')
            # print('error([输入数据长度与预定窗长不匹配。 预定窗长', str(self.window_step),' 实际输入数据长度',str(new_data.shape[1]),']')

        # 逐数据块去均值(整体去均值无法迭代)
        new_data = new_data - np.reshape(np.mean(new_data, 1), [new_data.shape[0], 1])

        # tic = datetime.datetime.now()
        equalized_new_data, self.equalized_data_zf = firfilter_matrix(self.spatio_temporal_equalizer, new_data, self.equalized_data_zf)
        # toc = datetime.datetime.now()
        # print('firfilter_matrix: ', toc-tic)

        self.equalized_data_R, x_G1, x_G2 = self.iterate_QR(self.equalized_data_R,equalized_new_data)
        x_G1_temp = np.empty((1,1), dtype=object)
        x_G2_temp = np.empty((1, 1), dtype=object)
        x_G1_temp[0, 0] = x_G1.H
        x_G2_temp[0, 0] = x_G2.H

        def for1(x, y, z):
            return x_G1.H * x * np.mat(y) + x_G2.H * np.mat(z)
            # 更新内积

        # tic = datetime.datetime.now()
        for template_index in range(0, len(self.template_set)):
            x = self.QxQy_inner_product_cell[template_index, range(self.current_max_window_index - 2, -1, -1)]
            y = self.template_G1[template_index, range(self.current_max_window_index - 1, 0, -1)]
            z = self.template_G2[template_index, range(self.current_max_window_index - 1, 0, -1)]
            self.QxQy_inner_product_cell[template_index, range(self.current_max_window_index - 1, 0, -1)] = x_G1_temp * x * y + x_G2_temp * z

            # m = map(for1, self.QxQy_inner_product_cell[template_index, range(self.current_max_window_index - 2, -1, -1)], self.template_G1[template_index, range(self.current_max_window_index - 1, 0, -1)], self.template_G2[template_index, range(self.current_max_window_index - 1, 0, -1)])
            #
            # self.QxQy_inner_product_cell[template_index, range(self.current_max_window_index - 1, 0, -1)] =[i for i in m]


            # self.QxQy_inner_product_cell[template_index, range(self.current_max_window_index - 1, 0, -1)] = list(m)

            # tic = datetime.datetime.now()
            self.QxQy_inner_product_cell[template_index,0] = x_G2.H * np.mat(self.template_G2[template_index,0])
            # toc = datetime.datetime.now()
            # print('xia:', toc - tic)
        # for template_index in range(0, len(self.template_set)):
        #
        #     for timestep_index in range(self.current_max_window_index - 1, 0, -1):
        #
        #         qxqy_old = self.QxQy_inner_product_cell[template_index, timestep_index - 1]
        #
        #         y_G1 = np.mat(self.template_G1[template_index, timestep_index])
        #
        #         y_G2 = np.mat(self.template_G2[template_index, timestep_index])
        #
        #         qxqy_new = x_G1.H * qxqy_old * y_G1 + x_G2.H * y_G2
        #         # print(self.template_G2[1,1])
        #         self.QxQy_inner_product_cell[template_index,timestep_index] = qxqy_new
        #
        #
        #     # obj.XY_InnerProductCell{templateIndex,1} = equalizedNewData * obj.templateSetpCell{templateIndex,1}';
        #     self.QxQy_inner_product_cell[template_index,0] = x_G2.H * np.mat(self.template_G2[template_index,0])


        # 更新信号能量
        # xx_new_engry = trace(equalizedNewData * equalizedNewData');
        # obj.XX_EnergyVector(2:obj.currentMaxWindowIndex) = obj.XX_EnergyVector(1:obj.currentMaxWindowIndex-1) + xx_new_engry;
        # obj.XX_EnergyVector(1) = xx_new_engry;

        if self.current_max_window_index < (self.max_window_length + self.offset)/self.window_step:
            self.current_max_window_index = self.current_max_window_index + 1
            self.reach_full_window_flag = False
        else:
            self.reach_full_window_flag = True

    def get_stop_values(self):
        if not self.reach_full_window_flag:
            max_window = self.current_max_window_index - 1
        else:
            max_window = self.current_max_window_index



        total_noise_energy = np.array(np.zeros((self.QxQy_inner_product_cell.shape[0], max_window)))

        def for1(x):
            return np.identity(x.shape[0]) - x * x.H

        for i in range(0, self.QxQy_inner_product_cell.shape[0]):
            # temp = np.array(np.zeros((max_window, self.channels_number, self.channels_number)), dtype=complex)
            # tic = datetime.datetime.now()

            x = self.QxQy_inner_product_cell[i, 0:max_window]
            # temp = np.array([i for i in map(for1, x)])
            temp = np.array(list(map(for1, x)))

            total_noise_energy[i, 0:max_window] = np.trace(np.real(temp), axis1=1, axis2=2)




        # for i in range(0, self.QxQy_inner_product_cell.shape[0]):
        #     for j in range(0, max_window):
        #     # for j in range(0, self.QxQy_inner_product_cell.shape[1]):
        #         x = np.mat(self.QxQy_inner_product_cell[i, j])
        #         total_noise_energy[i, j] = np.trace(np.identity(x.shape[0])-np.real(x*x.H))

        noise_energy_matrix = np.multiply(np.array(self.window_step * np.arange(1, max_window + 1)), total_noise_energy)
        min_noise_energy_vector = noise_energy_matrix.min(0)

        #原始判决准则(数据太小无法计算)
        # values = 1 - 1/np.sum(np.exp(-0.5 * (bsxfun(@minus,noiseEnergyMatrix ,minNoiseEnergyVector))),1);
        #

        sum_probability = np.sum(np.exp(-0.5 * (noise_energy_matrix - min_noise_energy_vector)),axis=0)

        # 最终判决准则 log(sumProbability) <  -log(1-threshold)) 可以有效避免数值稳定性问题

        log_sum_probability = np.log(sum_probability)
        return log_sum_probability

    def classify(self):
        if not self.reach_full_window_flag:
            max_window = self.current_max_window_index - 1
        else:
            max_window = self.current_max_window_index


        signal_energy_cell = np.array(
            np.zeros((self.QxQy_inner_product_cell.shape[0], max_window)))

        def for1(x):
            return x * x.H

        for i in range(0, self.QxQy_inner_product_cell.shape[0]):
            # temp = np.array(np.zeros((max_window, self.channels_number, self.channels_number)), dtype=complex)
            # tic = datetime.datetime.now()
            x = self.QxQy_inner_product_cell[i, 0:max_window]
            temp = np.array(list(map(for1, x)))
            # temp = np.array([i for i in map(for1, x)])

            signal_energy_cell[i, 0:max_window] = np.linalg.eigvals(np.real(temp)).max(1)
        toc = datetime.datetime.now()

                # signal_energy_cell[i, j] = np.linalg.eigh(np.real(x * x.H))[0].max()

        # for i in range(0, self.QxQy_inner_product_cell.shape[0]):
        #     for j in range(0, max_window):
        #         x = np.mat(self.QxQy_inner_product_cell[i, j])
        #         signal_energy_cell[i, j] = np.linalg.eigh(np.real(x * x.H))[0].max()
        # time.sleep(0.02)

        result_vector = np.argmax(signal_energy_cell, axis=0)

        return result_vector

    def clear(self):
        self.reach_full_window_flag = False

        # 初始化内积组合
        self.QxQy_inner_product_cell = np.empty((40, int((self.max_window_length + self.offset) / self.window_step)), dtype=object)
        for i in range(0, self.QxQy_inner_product_cell.shape[0]):
            for j in range(0, self.QxQy_inner_product_cell.shape[1]):
                self.QxQy_inner_product_cell[i,j] = np.mat(np.zeros((self.channels_number,self.channels_number)))

        self.current_max_window_index = 1

        # 初始化均衡数据参数
        self.equalized_data_zf = None

        self.equalized_data_R = None

    def set_spatio_temporal_equalizer(self,spatio_temporal_equalizer):
        self.spatio_temporal_equalizer = spatio_temporal_equalizer

    def set_template_set(self,template_set):

        self.template_set =  template_set

        # 计算模板QR分解
        self.template_set_p_cell = np.empty((len(self.template_set), int((self.max_window_length + self.offset) / self.window_step)), dtype=object)
        # np.empty((len(self.template_set), int((self.max_window_length + self.offset) / self.window_step)), dtype=object)
        self.template_G1 = np.empty((len(self.template_set), int((self.max_window_length + self.offset) / self.window_step)), dtype=object)

        self.template_G2 = np.empty((len(self.template_set), int((self.max_window_length + self.offset) / self.window_step)), dtype=object)

        for template_index in range(0, len(self.template_set)):

            template = self.template_set[template_index]

            # 截取最大长度
            template = template[:,0:self.max_window_length + self.offset]

            template_extend = np.reshape(np.array(template), (template.shape[0], int(self.window_step), int((self.max_window_length + self.offset)/self.window_step)), order='F')

            # R = np.identity(self.channels_number)
            R = None
            t = template_extend[...,1]
            # print(t)
            for timestep_index in range(0, template_extend.shape[2]):

                self.template_set_p_cell[template_index, timestep_index] = template_extend[...,timestep_index]
                # print(self.template_set_p_cell[template_index,timestep_index])
                R, tg1, tg2 = self.iterate_QR(R, self.template_set_p_cell[template_index,timestep_index])
                self.template_G1[template_index,timestep_index]=tg1
                self.template_G2[template_index,timestep_index]=tg2

    # def iterate_QR(self, R, new_data):
    #     new_data = np.mat(new_data)
    #
    #     if R is None:
    #         G1_size = 0
    #         R = new_data.H
    #     else:
    #         G1_size = R.shape[0]
    #         R = np.vstack((R, new_data.H))
    #
    #     G,R_new = np.linalg.qr(R, mode='reduced')  # !!!!!!!!!!
    #     # matlabQR分解会重排矩阵，还原重排结果
    #     # E = np.identity(R_new.shape[1]))
    #     # E = E(:,e);
    #     # Rnew = Rnew * E';
    #     if G1_size == 0:
    #         G1 = np.zeros((self.channels_number,self.channels_number))  # np.mat(np.identity(self.channels_number))
    #     else:
    #         G1 = G[0:G1_size, :]
    #     G2 = G[G1_size:, :]
    #     return R_new, G1, G2

    def iterate_QR(self, R, new_data):
        new_data = np.mat(new_data)

        if R is None:
            G1_size = 0
            R = new_data.H
        else:
            G1_size = R.shape[0]
            R = np.vstack((R, new_data.H))

        G, R_new, e = scl.qr(R, mode='economic', pivoting=True)  # !!!!!!!!!!
        # matlabQR分解会重排矩阵，还原重排结果
        E = np.identity(R_new.shape[1])
        E = np.mat(E[:, e])
        R_new = R_new * E.H
        if G1_size == 0:
            G1 = np.zeros((8, 8))  # np.mat(np.identity(self.channels_number))
        else:
            G1 = G[0:G1_size, :]
        G2 = G[G1_size:, :]
        return np.mat(R_new), np.mat(G1), np.mat(G2)



