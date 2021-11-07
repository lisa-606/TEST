from abc import ABCMeta, abstractmethod


class BasicAnalysisProcess:
    def __init__(self):
        self.real_time_reader = None
        self.experiment_information = None

        self.controller = None
        self.schema_controller = None

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def run(self):
        pass

    def initial(self, experiment_information = None, real_time_reader = None):
        self.experiment_information = experiment_information
        self.real_time_reader = real_time_reader

        # self.controller = singleton_analysis_controller
        # self.schema_controller = singleton_schema_controller
