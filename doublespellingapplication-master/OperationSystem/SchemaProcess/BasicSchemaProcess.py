from abc import ABCMeta, abstractmethod


class BasicSchemaProcess:
    def __init__(self):
        self.analysis_controller = None
        self.schema_controller = None

    def initial(self):
        pass
        # self.analysisController = singleton_analysis_controller
        # self.schemaController = singleton_schema_controller

    @abstractmethod
    def get_analysis_updata_obj(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def over(self):
        pass

    @abstractmethod
    def report(self):
        pass