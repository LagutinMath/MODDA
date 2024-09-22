import numpy as np
from modda.data_handler.Model import Model


class InvCosModel(Model):
    def __init__(self, D, theta, gamma, rate, wavelength, local_time_range, global_time_range, data_time_range):
        super().__init__(local_time_range, global_time_range, data_time_range)
        self.D = D
        self.theta = theta
        self.gamma = gamma
        self.rate = rate
        self.wavelength = wavelength

    @classmethod
    def init_coef(cls, dep_data, layer=1):
        y_data = dep_data.measurements[layer].y_data

        T_min = min(y_data)
        T_max = max(y_data)
        A = T_max - T_min

        gamma_0 = 0.5 * (1 / T_min + 1 / T_max)
        D_0 = 0.5 * (1 / T_min - 1 / T_max)

        S_0 = (T_max - y_data[0]) / A
        nu_0 = 1 / (T_max - S_0 * A)
        theta_0 = np.arccos((nu_0 - gamma_0) / D_0)

        # rate_0 = dep_data.design.thicknesses[layer] / (dep_data.final_time[layer] - dep_data.start_time[layer])
        rate_0 = np.pi / (dep_data.final_time[layer] - dep_data.start_time[layer])
        wavelength_0 = dep_data.measurements[layer].wave.wavelength

        local_time_range, global_time_range, data_time_range = Model.grid_from_dep(dep_data, layer)

        return cls(D_0, theta_0, gamma_0, rate_0, wavelength_0, local_time_range, global_time_range, data_time_range)

    def get_param(self):
        return {'D': {'name': 'D', 'lb': 0, 'rb': 1, 'prec': 2},
                'theta': {'name': 'theta', 'lb': 0, 'rb': 2 * np.pi, 'prec': 2},
                'gamma': {'name': 'gamma', 'lb': 0, 'rb': 2, 'prec': 4},
                'rate': {'name': 'rate', 'lb': 0., 'rb': 0.01, 'prec': 4}}

    def calc(self, t):
        """Calculate transmittance (T) from time (t)"""
        # return 1. / (self.D * np.cos(2 * np.pi * self.rate * t / self.wavelength + self.theta) + self.gamma)
        return 1. / (self.D * np.cos(self.rate * t + self.theta) + self.gamma)

    def update(self, kwargs):
        for kwarg in kwargs:
            self.__dict__[kwarg] = kwargs[kwarg]

    def optimize(self):
        pass


