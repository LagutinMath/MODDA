import json
import zipfile
from dataclasses import dataclass
from Wave import Wave
from datetime import datetime
import numpy as np
import paths as config


@dataclass
class LayerMeasurements:
    layer: int
    wave: Wave
    t: np.ndarray
    y_data: np.ndarray
    type_of_y: str


class DepositionMeasurements:
    def __init__(self, comment, date, measurements):
        self.comment = comment
        self.date = date
        self.measurements = measurements

    @classmethod
    def from_dict(cls, data):
        comment = data['comment']
        date = datetime.strptime(data['date'], '%Y-%m-%d')
        measurements = {}
        meas_data = data['measurements']
        for meas in meas_data:
            type_of_y = 'T' if 'T' in meas else 'R'
            measurements[meas['layer']] = LayerMeasurements(layer=meas['layer'],
                                                            wave=Wave(wavelength=meas['Wave']['wavelength'],
                                                                      polarisation=Wave.Pol.from_str(
                                                                          meas['Wave']['polarisation']),
                                                                      angle=Wave.Angle(meas['Wave']['angle'])),
                                                            t=np.array(meas['t']),
                                                            y_data=np.array(meas[type_of_y]),
                                                            type_of_y=type_of_y)
        return cls(comment, date, measurements)

    @classmethod
    def from_dep(cls, file_path):
        data = cls.load_dep_file(file_path)
        return cls.from_dict(data)

    @staticmethod
    def save_dep_file(data, file_path):
        """
        Saves data to a .dep file, compressed with JSON in ZIP.

        :param data: Dictionary with data.

        :param file_path: Path to the .dep file.
        """
        try:
            json_data = json.dumps(data, ensure_ascii=False, indent=2)

            with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_LZMA) as zipf:
                zipf.writestr('data.json', json_data)

            print(f"File saved as{file_path}")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def load_dep_file(file_path):
        """
        Loads data from the .dep file.

        :param file_path: Path to the .dep file.
        :return: Dictionary with data.
        """
        if not file_path.endswith('.dep'):
            print("Invalid file extension. Expecting .dep")
            return None
        try:
            with zipfile.ZipFile(file_path, 'r') as zipf:
                with zipf.open('data.json') as json_file:
                    data = json.load(json_file)
            return data
        except Exception as e:
            print(f"Error: {e}")
            return None


if __name__ == '__main__':
    ms = DepositionMeasurements.from_dep(config.meas_dir + '/' + '24_03-AR_4_Zh.dep')
    print(ms.measurements[1].layer)
