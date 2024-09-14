import numpy as np
import os.path
import json
from modda.data_handler.Material import Material
import modda.paths as config


class Design:
    __slots__ = ('thicknesses', '_materials', 'structure', 'name')

    def __init__(self, thicknesses, materials, structure='HL', name=None):
        self.name = name
        # thicknesses - np.array
        self.thicknesses = thicknesses
        N = len(thicknesses) - 1
        # materials : {'substrate': D263T, 'H': Nb2O5, 'L': SiO2}
        self._materials = materials
        self.structure = 'S' + (structure * (N // len(structure) + 1))[:N]

    @classmethod
    def from_dict(cls, data):
        name = data['name']
        thicknesses = np.array(data['thicknesses'])

        if 'mat_inf' in data:
            materials_by_names = {name: Material.linear_interp(data['mat_inf'][name], name)
                                  for name in data['mat_inf']}
            roles = Design.get_roles(data['layers'], materials_by_names)
            materials = {roles[name]: materials_by_names[name]
                         for name in materials_by_names}
            structure = ''.join([roles[layer_mat]
                                 for layer_mat in data['layers'][1:]])

        return cls(thicknesses, materials, structure, name)

    @classmethod
    def from_json(cls, name):
        des_file = os.path.join(config.des_dir, f'{name}.json')
        with open(des_file, encoding='utf-8') as file:
            data = json.load(file)
        return cls.from_dict(data)

    @staticmethod
    def get_roles(layers, materials_by_names):
        roles_list = list('HLABCDEF')
        sorted_mat = sorted(list(set(layers[1:])),
                            key=lambda name: materials_by_names[name].avr_n(),
                            reverse=True)
        return dict([(layers[0], 'substrate')] +
                    list(zip(sorted_mat, roles_list)))

    @property
    def N(self):
        return len(self.thicknesses) - 1

    def d(self, j):
        return self.thicknesses[j]

    def n(self, j, wavelen):
        if not j:
            return self.n_s(wavelen)
        return self._materials[self.structure[j]].n(wavelen)

    def xi(self, j, wavelen):
        if not j:
            return self.xi_s(wavelen)
        return self._materials[self.structure[j]].xi(wavelen)

    def n_s(self, wavelen):
        return self._materials['substrate'].n(wavelen)

    def xi_s(self, wavelen):
        return self._materials['substrate'].xi(wavelen)

    def layer_role(self, j):
        return self.structure[j]


if __name__ == '__main__':
    des = Design.from_json('NF122')
    print(des.name)
    print(des.thicknesses)
    print(des.structure)
    print(des.n(1, 500))
    print(des.layer_role(1))

    # Design.from_dict()
    # Design.from_json()
    # des.to_json()
