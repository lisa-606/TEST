from doubleSpellingApplication.OperationSystem.AnalysisProcess.BasicAnalysisProcess import BasicAnalysisProcess
import datetime
import time
import logging


class WaitAnalysisProcess(BasicAnalysisProcess):
    def __init__(self):
        self.operator_method = None
        self.operation_state = None

        self.logger = logging.getLogger("DoubleSpellingApplication.WaitAnalysisProcess")

    def initial(self, analysis_controller, schema_controller, experiment_iInformation, real_time_reader, operation_state, operator_method):
        self.logger.debug("WaitAnalysisProcess.initial is called.")
        BasicAnalysisProcess.initial(self, experiment_iInformation, real_time_reader)
        self.analysis_controller = analysis_controller
        self.schema_controller = schema_controller
        self.operation_state = operation_state
        self.operator_method = operator_method

    def update(self, analysis_process_updata_obj):
        pass

    def run(self):

        self.logger.debug('进入等待模式,{0}\n'.format(datetime.datetime.now()))

        while (self.operation_state.current_detect_state != 'STRD') and (self.operation_state.control_state != 'EXIT'):
            time.sleep(0.1)


        self.analysis_controller.detect_analysis_process.clear()
        self.analysis_controller.current_analysis_process = self.analysis_controller.detect_analysis_process