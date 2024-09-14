from PySide6.QtWidgets import QWidget, QVBoxLayout
from modda.gui.MainPlot import MainPlot


class MainPlotSection(QWidget):
    def __init__(self, program_data):
        super().__init__()

        self.program_data = program_data

        self.layout = QVBoxLayout(self)
        self.plot = MainPlot(self.program_data)
        self.layout.addWidget(self.plot)

