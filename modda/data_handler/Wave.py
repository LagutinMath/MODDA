from __future__ import annotations
from functools import total_ordering
from enum import Enum
from math import pi


@total_ordering
class Wave:
    __slots__ = ('_wavelength', '_polarisation', '_angle')

    class Pol(Enum):
        S: int = 1
        P: int = 2

        @staticmethod
        def from_str(letter: str) -> Wave.Pol:
            if letter == 'S':
                return Wave.Pol.S
            if letter == 'P':
                return Wave.Pol.P
            raise ValueError('Polarisation can be only S or P')

        def __str__(self):
            return self.name

        def __repr__(self):
            if self.name == 'S':
                return 'Wave.Pol.S'
            else:
                return 'Wave.Pol.P'

    @total_ordering
    class Angle:
        __slots__ = ('_value', )

        class Unit(Enum):
            RAD: int = 1
            DEG: int = 2

        def __init__(self, value: int | float = 0.0, unit: Unit = Unit.RAD):
            if unit not in (self.Unit.RAD, self.Unit.DEG):
                raise TypeError

            if unit is self.Unit.RAD:
                if 0. <= value < 0.5 * pi:
                    self._value: float = float(value)
                else:
                    raise ValueError
            elif unit is self.Unit.DEG:
                if 0. <= value < 90.:
                    self._value: float = self.change_unit(value, self.Unit.RAD)
                else:
                    raise ValueError

        def __lt__(self, other: Wave.Angle):
            if isinstance(other, Wave.Angle):
                return self._value < other._value
            return NotImplemented

        def is_normal(self) -> bool:
            if self._value == 0:
                return True
            return False

        @staticmethod
        def change_unit(value: int | float, out_unit: Unit) -> float:
            if out_unit is Wave.Angle.Unit.DEG:
                return value * 180. / pi
            if out_unit is Wave.Angle.Unit.RAD:
                return value * pi / 180.
            raise TypeError

        def __str__(self, unit: Unit = Unit.DEG):
            value = self._value if unit is self.Unit.RAD else self.change_unit(self._value, unit)
            return f'{value:.1f} {unit.name}'

        def __repr__(self):
            return f"Wave.Angle({self._value}, Wave.Angle.Unit.RAD)"

    def __init__(self, wavelength: int | float, polarisation: Pol = Pol.S, angle: Angle = Angle(0.)):
        """Incident wave class
        :param wavelength: wavelength in nm
        :param polarisation: 'S' or 'P' polarisation
        :param angle: angle in radians
        """
        self._wavelength: int | float = wavelength
        self._polarisation: Wave.Pol = polarisation
        self._angle: Wave.Angle = angle

    @property
    def wavelength(self) -> float:
        return self._wavelength

    @property
    def polarisation(self) -> Wave.Pol:
        return self._polarisation

    @property
    def angle(self) -> Wave.Angle:
        return self._angle

    def __float__(self):
        return float(self.wavelength)

    def __str__(self):
        if self.angle.is_normal():
            return f'{self.wavelength} nm'
        return f'{self.wavelength} nm, polarisation: {self.polarisation}, {self.angle}'

    def __repr__(self):
        return f'Wave({self.wavelength}, {self.polarisation!r}, {self.angle!r})'

    def __eq__(self, other: Wave):
        if isinstance(other, Wave):
            return (self.wavelength == other.wavelength and
                    self.polarisation is other.polarisation and
                    self.angle == other.angle)
        return NotImplemented

    def __hash__(self):
        return hash((self.wavelength, self.polarisation, self.angle))

    def __lt__(self, other: Wave):
        if isinstance(other, Wave):
            if self.angle > other.angle:
                return True
            if self.polarisation is not other.polarisation and other.polarisation is Wave.Pol.P:
                return True
            return self.wavelength < other.wavelength
        return NotImplemented

    def __add__(self, other: int | float) -> Wave:
        if isinstance(other, (int, float)):
            return Wave(self.wavelength + other, self.polarisation, self.angle)
        return NotImplemented

    def __radd__(self, other: int | float) -> Wave:
        return self.__add__(other)

    def __sub__(self, other: int | float) -> Wave:
        if isinstance(other, (int, float)):
            return Wave(self.wavelength - other, self.polarisation, self.angle)
        return NotImplemented

    def __rsub__(self, other: int | float) -> Wave:
        if isinstance(other, (int, float)):
            return Wave(other - self.wavelength, self.polarisation, self.angle)
        return NotImplemented


if __name__ == '__main__':
    print(dir(Wave))
    wv_ang: Wave.Angle = Wave.Angle(pi / 3)
    print(f'{wv_ang = !s}')
    print(f'{wv_ang = !r}')

    wv_pol: Wave.Pol = Wave.Pol.from_str('S')
    print(f'{wv_pol = !s}')
    print(f'{wv_pol = !r}')

    wv_1: Wave = Wave(500)
    print(f'{wv_1 = !s}')
    print(f'{wv_1 = !r}')
    print(f'{wv_1 == Wave(500) = }')
    wv_2 = Wave(500, Wave.Pol.P)
    print(f'{wv_1 < wv_2 = }')
    print(f'{hash(wv_1) = }')
    print(f'{Wave(500) + 4 = }')

    wv_3: Wave = Wave(500, angle=Wave.Angle(45, Wave.Angle.Unit.DEG))
    print(f'{wv_3 = !s}')
    print(f'{wv_3 = !r}')
