from doubleSpellingApplication.OperationSystem.AnalysisProcess.OperatorMethod.MultilayerWindowClassifierParameters import MultilayerWindowClassifierParameters
from doubleSpellingApplication.OperationSystem.AnalysisProcess.DetectAnalysisProcess import DetectAnalysisProcess
from doubleSpellingApplication.OperationSystem.AnalysisProcess.UpdateAnalysisProcess import UpdateAnalysisProcess
from doubleSpellingApplication.OperationSystem.AnalysisProcess.WaitAnalysisProcess import WaitAnalysisProcess
from doubleSpellingApplication.OperationSystem.AnalysisProcess.OperatorMethod.MultilayerWindowClassifier import MultilayerWindowClassifier
import logging


class AnalysisController:
    def __init__(self):
        self.current_analysis_process = None
        self.operator_method = None

        self.detect_analysis_process = None
        self.update_analysis_process = None
        self.wait_analysis_process = None

        self.logger = logging.getLogger("DoubleSpellingApplication.AnalysisController")

    def initial(self, schema_controller, experiment_information, real_time_reader, operation_state, process_monitor_information):
        self.logger.debug("AnalysisController.initial is called.")

        self.current_analysis_process = None
        self.operator_method = None

        self.detect_analysis_process = None
        self.update_analysis_process = None
        self.wait_analysis_process = None

        multilayer_window_classifier_parameters = MultilayerWindowClassifierParameters()
        multilayer_window_classifier_parameters.window_step = experiment_information.window_step_time * experiment_information.down_frequency_sample
        multilayer_window_classifier_parameters.max_window_length = experiment_information.max_window_time * experiment_information.down_frequency_sample
        multilayer_window_classifier_parameters.channels_number = experiment_information.channel_no
        multilayer_window_classifier_parameters.offset = experiment_information.offset_time * experiment_information.down_frequency_sample
        multilayer_window_classifier_parameters.equalizer_order = experiment_information.equalizer_order

        self.operator_method = MultilayerWindowClassifier()
        self.operator_method.initial(multilayer_window_classifier_parameters)

        self.detect_analysis_process = DetectAnalysisProcess()

        self.detect_analysis_process.initial(self, schema_controller, experiment_information, real_time_reader, operation_state, self.operator_method, process_monitor_information)

        self.update_analysis_process = UpdateAnalysisProcess()

        self.update_analysis_process.initial(self, schema_controller, experiment_information, real_time_reader, self.operator_method)

        self.wait_analysis_process = WaitAnalysisProcess()
        self.wait_analysis_process.initial(self, schema_controller, experiment_information, real_time_reader, operation_state, self.operator_method)


        self.current_analysis_process = self.wait_analysis_process

    def update(self, analysis_process_updata_obj):

        if analysis_process_updata_obj.STEqualizer is not None:
            self.operator_method.set_spatio_temporal_equalizer(analysis_process_updata_obj.STEqualizer)


        if analysis_process_updata_obj.target_template_set is not None:
            self.operator_method.set_template_set(analysis_process_updata_obj.target_template_set)

        self.detect_analysis_process.update(analysis_process_updata_obj)

        self.update_analysis_process.update(analysis_process_updata_obj)

        self.wait_analysis_process.update(analysis_process_updata_obj)

    def run(self):
        self.current_analysis_process.run()
