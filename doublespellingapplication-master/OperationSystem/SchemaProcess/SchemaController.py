from doubleSpellingApplication.OperationSystem.SchemaProcess.DoubleSpellingSchemaProcess import DoubleSpellingSchemaProcess
from doubleSpellingApplication.CommonSystem.CommonModule.ResultTransferModel import ResultTransferModel
import datetime
import logging


class SchemaController:
    def __init__(self):
        self.schema_process_list = []
        self.exchange_message_management = None

        self.current_schema_process = None
        self.save_struct = None

        self.logger = logging.getLogger("DoubleSpellingApplication.SchemaController")

    def initial(self, experiment_information, exchange_message_management):
        self.schema_process_list = []
        self.exchange_message_management = None

        self.current_schema_process = None
        self.save_struct = None

        self.logger.debug("SchemaController.initial is called.")
        self.exchange_message_management = exchange_message_management
        self.schema_process_list.append(DoubleSpellingSchemaProcess())

        for i in range(0, len(self.schema_process_list)):
            self.schema_process_list[i].initial(experiment_information, self.exchange_message_management)

        self.current_schema_process = self.schema_process_list[0]

    def get_analysis_update_obj(self):
        analysis_update_obj = self.current_schema_process.get_analysis_updata_obj()
        return analysis_update_obj

    def clear(self):

        for i in range(0, len(self.schema_process_list)):
            self.schema_process_list[i].clear()

        result_id = None  #[]
        result_obj = self.current_schema_process.report(result_id)

        result_transfer_model = self.create_result_transfer_model(result_obj)
        #message_body = ResultTransferModelConvertor.toMessage(resultTransferModel);
        #message = ToStimulationSendingExchangeMessage.FeedbackResult.setMessage(messageBody);
        #self.exchange_message_management.sendExchangeMessage(message);

        self.logger.debug('\n{0}.clear:\n当前刺激模式{1}s\n发送\n'.format(self.__class__.__name__, self.current_schema_process.__class__.__name__))

    def report(self, result_id):

        result_obj = self.current_schema_process.report(result_id)

        #resultTransferModel = obj.createResultTransferModel(result_obj)

        self.logger.debug('\n{0}.report:\n当前刺激模式{1},执行时间{2}\n\n\n'.format(self.__class__.__name__, self.current_schema_process.__class__.__name__, datetime.datetime.now()))

        #message_body = ResultTransferModelConvertor.toMessage(resultTransferModel);


    def set_current_schema_processes(self, schema_process):
        self.current_schema_process = schema_process
        self.logger.debug('\nSchemaController.setCurrentSchemaProcesses:\n当前处理模式被设定为:%s\n'.format(schema_process.__class__.__name__))

    def create_result_transfer_model(result_obj):
        result_transfer_model = ResultTransferModel()
        result_transfer_model.prepare_last_time = result_obj.prepare_last_time
        result_transfer_model.finish_last_time = result_obj.finish_last_time
        result_transfer_model.alphabet_id = result_obj.alphabet_id
        return result_transfer_model


