from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PySide6.QtCore import Qt
from collections import namedtuple

LabeledSlider = namedtuple('LabeledSlider', ['label', 'slider'])


class ModelSliders(QWidget):
    def __init__(self, plot_widget):
        super().__init__()

        self.plot_widget = plot_widget

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.labeled_sliders = self.create_sliders()

        for label, slider in self.labeled_sliders.values():
            self.layout.addWidget(label)
            self.layout.addWidget(slider)

    def create_sliders(self):
        sliders = dict()
        model_vars = self.plot_widget.model.__dict__.copy()
        for variable in model_vars:
            sliders[variable] = LabeledSlider(QLabel(""),
                                              QSlider(Qt.Horizontal))

            sliders[variable].slider.setRange(0, 100)
            sliders[variable].slider.setValue(10)
            sliders[variable].label.setText(f"{variable} = "
                                            f"{model_vars[variable] * sliders[variable].slider.value() / 10.0:.3f}")

            sliders[variable].slider.valueChanged.connect(lambda value, var=variable:
                                                          sliders[var].label.setText(
                                                              f"{var} = {model_vars[var] * value / 10.0:.3f}"))

            sliders[variable].slider.valueChanged.connect(lambda value, var=variable:
                                                          self.plot_widget.update_curve({var: (model_vars[var] * value / 10.0)}))

        return sliders
