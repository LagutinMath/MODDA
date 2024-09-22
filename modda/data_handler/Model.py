from abc import ABC, abstractmethod
import numpy as np


class Model(ABC):
    def __init__(self, local_time_range, global_time_range, data_time_range):
        self.name = self.__class__.__name__
        self.local_time_range = local_time_range
        self.global_time_range = global_time_range
        self.data_time_range = data_time_range

    @staticmethod
    def grid_from_dep(dep_data, layer=None):
        global_time_range = np.arange(dep_data.start_time[1], dep_data.final_time[dep_data.design.N], 0.1)
        if layer is not None:
            local_time_range = np.arange(dep_data.start_time[layer], dep_data.final_time[layer], 0.1)
            data_time_range = dep_data.get_consequent_x_data(layer)
        else:
            local_time_range = global_time_range
            data_time_range = dep_data.get_whole_time_range()
        return local_time_range, global_time_range, data_time_range

    @abstractmethod
    def calc(self, x):
        """Calculate y(x) for model"""
        pass

    def calc_ltr(self):
        """Calculate y_data on local_time_range x_data grid"""
        x_data = self.local_time_range
        return x_data, np.vectorize(self.calc)(x_data)

    def calc_gtr(self):
        """Calculate y_data on global_time_range x_data grid"""
        x_data = self.global_time_range
        return x_data, np.vectorize(self.calc)(x_data)

    def calc_dtr(self):
        """Calculate y_data on data_time_range x_data grid"""
        x_data = self.data_time_range
        return x_data, np.vectorize(self.calc)(x_data)

    @abstractmethod
    def optimize(self):
        """Optimize params from current point"""
        pass

    def save(self, filename):
        """Save data to .mdl file"""
        pass

    def load(self, filename):
        """Load data from .mdl file"""
        pass
