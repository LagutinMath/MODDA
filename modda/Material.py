import json
import scipy
import numpy as np
from tools import timer
import os
from paths import des_dir


class Material:
    def __init__(self, n_func, xi_func, boundaries, name=None):
        self.name = name
        self.boundaries = boundaries

        self._cache = dict()
        self._n = n_func
        self._xi = xi_func

    @classmethod
    def linear_interp(cls, ri_dict, name=None):
        # ri_dict struct: {'Table': {'wavelength': [...]
        #                           'n': [...],
        #                           'xi': [...]}}

        if 'Table' in ri_dict:
            wavelength = ri_dict['Table']['wavelength']
            boundaries = (min(wavelength),
                          max(wavelength))

            if 'n' in ri_dict['Table']:
                n_func = scipy.interpolate.make_interp_spline(
                    wavelength,
                    ri_dict['Table']['n'],
                    k=1)
            else:
                n_func = Material.const_func(0.)

            if 'xi' in ri_dict['Table']:
                xi_func = scipy.interpolate.make_interp_spline(
                    wavelength,
                    ri_dict['Table']['xi'],
                    k=1)
            else:
                xi_func = Material.const_func(0.)

            return cls(n_func, xi_func, boundaries, name)

        if 'const' in ri_dict:
            boundaries = (1.,
                          2500.)

            n_func = Material.const_func(ri_dict['const'].get('n', 0.))
            xi_func = Material.const_func(ri_dict['const'].get('xi', 0.))

            return cls(n_func, xi_func, boundaries, name)


    @classmethod
    def const(cls, n, xi=0., name=None):
        boundaries = (0, np.inf)
        n_func = Material.const_func(n)
        xi_func = Material.const_func(xi)
        return cls(n_func, xi_func, boundaries, name)

    def put_in_cache(self, wavelen):
        self._cache[wavelen] = (self._n(wavelen), self._xi(wavelen))

    def n(self, wavelen):
        if wavelen not in self._cache:
            self.put_in_cache(wavelen)
        return self._cache[wavelen][0]

    def xi(self, wavelen):
        if wavelen not in self._cache:
            self.put_in_cache(wavelen)
        return self._cache[wavelen][1]

    def avr_n(self):
        left = self.boundaries[0]
        right = self.boundaries[-1] if self.boundaries[-1] != np.inf else self.boundaries[0]
        return 0.5 * (self.n(right) + self.n(left))

    @staticmethod
    def const_func(const=0.):
        def func(x):
            return const
        return func


if __name__ == '__main__':

    with open(os.path.join(des_dir, 'NF122.json')) as f:
        des_data = json.load(f)

    # print(des_data['mat_inf']['D263T'])
    mat = Material.linear_interp(des_data['mat_inf']['D263T'], name='D263T')
    timer(100_000)(mat.n)(525)

    mat_2 = Material.const(2.1, name='D263T')
    timer(100_000)(mat.n)(525)
    # Mean time: 3.6e-06 sec
    # Mean time: 2.2e-07 sec
