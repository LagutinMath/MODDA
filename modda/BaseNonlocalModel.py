import numpy as np

class BaseNonlocalModel:
    def __init__(self, D, theta, gamma, rate, wavelength):
        self.D = D
        self.theta = theta
        self.gamma = gamma
        self.rate = rate
        self.wavelength = wavelength

    def T(self, t):
        # return 1. / (self.D * np.cos(2 * np.pi * self.rate * t / self.wavelength + self.theta) + self.gamma)
        return 1. / (self.D * np.cos(self.rate * t + self.theta) + self.gamma)

    def update(self, kwargs):
        for kwarg in kwargs:
            self.__dict__[kwarg] = kwargs[kwarg]

    @classmethod
    def init_coef(cls, dep_data, layer):
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

        return cls(D_0, theta_0, gamma_0, rate_0, wavelength_0)

    def get_xy_data(self, start, end):
        x_data = np.arange(start, end, 0.1)
        return x_data, np.vectorize(self.T)(x_data)


