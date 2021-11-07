from abc import ABCMeta, abstractmethod


class RealTimeReaderInterface:
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def read_raw_data(self, start_point, end_point):
        pass

    @abstractmethod
    def read_new_raw_data(self, point_count):
        pass

    @abstractmethod
    def read_fixed_length_raw_data(self, start_point, length):
        pass

    @abstractmethod
    def get_data_size(self):
        pass  # 1

    @abstractmethod
    def get_stored_data_head_trail_point(self):
        pass

    @abstractmethod
    def read_data(self, start_point, end_point):
        pass  # 1

    @abstractmethod
    def read_new_data(self, point_count):
        pass  # 1从尾巴取

    @abstractmethod
    def read_fixed_length_data(self, start_point, length):
        pass  # 1从起点取一定长度