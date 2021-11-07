class ExperimentInformation:
    def __init__(self):
        self.experiment_name = 'UAVControl'
        self.description = '无人机飞行控制'
        self.serial_port = None

        self.stimulation_frequency_set = None
        self.stimulation_phase_set = None
        self.schema_process_information = None
        self.alphabet_information_table = None
        self.frame_rate = None
        self.prepare_last_time = None
        self.stimulation_max_time = None
        self.finish_last_time = None
        self.save_path = None
        #self.view_object_path = None
        self.preprocess_filter = None

        #self.stimulation_record_table = {}
        self.experiment_start_time = None
        self.experiment_end_time = None
        self.operation_time_record = None

    #def set_stimulation_record_table(self, record):
