from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PySide6.QtCore import Qt
from collections import namedtuple

LabeledSlider = namedtuple('LabeledSlider', ['label', 'slider'])


class ModelSliders(QWidget):
    def __init__(self, program_data):
        super().__init__()
        self.program_data = program_data

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.labeled_sliders = self.create_sliders()

        for label, slider in self.labeled_sliders.values():
            self.layout.addWidget(label)
            self.layout.addWidget(slider)

    def create_sliders(self):
        sliders = dict()
        model_data = self.program_data.models[0].__dict__.copy()
        model_param = self.program_data.models[0].get_param()
        for variable in model_param:
            sliders[variable] = LabeledSlider(QLabel(model_param[variable]['name']),
                                              QSlider(Qt.Horizontal))

            num_steps = 1000

            sliders[variable].slider.setRange(1, num_steps)
            init_position = self.to_slider_value(model_data[variable], variable, model_param, num_steps)
            sliders[variable].slider.setValue(init_position)

            sliders[variable].label.setText(f"{model_param[variable]['name']} = "
                                            f"{self.from_slider_value(init_position, variable, model_param, num_steps)
                                            :.{model_param[variable]['prec']}f}")

            sliders[variable].slider.valueChanged.connect(lambda value, var=variable:
                                                          sliders[var].label.setText(
                                                              f"{model_param[var]['name']} = "
                                                              f"{self.from_slider_value(value, var, model_param, num_steps)
                                                              :.{model_param[var]['prec']}f}"
                                                          ))

            sliders[variable].slider.valueChanged.connect(lambda value, var=variable:
                                                          self.program_data.model_changed.emit({var: self.from_slider_value(value,
                                                                                                               var,
                                                                                                               model_param,
                                                                                                               num_steps)}))

        return sliders

    @staticmethod
    def to_slider_value(x, variable, model_param, num_steps):
        lb = model_param[variable]['lb']
        rb = model_param[variable]['rb']
        return round(((rb - x) + num_steps * (x - lb)) / (rb - lb))

    @staticmethod
    def from_slider_value(n, variable, model_param, num_steps):
        lb = model_param[variable]['lb']
        rb = model_param[variable]['rb']
        return (lb * (num_steps - n) + rb * (n - 1)) / (num_steps - 1)
