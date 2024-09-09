from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QFileDialog)
from PySide6.QtGui import QAction
from DepositionMeasurements import DepositionMeasurements
from paths import meas_dir
import os
from MainPlot import MainPlot
from BaseNonlocalModel import BaseNonlocalModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create layout and menu
        self.create_menu()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        file_name = '24_03-AR_4_Zh.dep'
        default_data = DepositionMeasurements.from_dep(os.path.join(meas_dir, file_name))
        default_model = BaseNonlocalModel.init_coef(default_data, 1)

        # Initialize plot widget with white background
        self.dep_data = default_data
        self.model = default_model
        self.plot_widget = MainPlot(self.dep_data, self.model)
        self.layout.addWidget(self.plot_widget)

        # self.sliders = ModelSliders()
        # self.layout.addWidget(self.sliders)

    def create_menu(self):
        # Create the menu bar and add File menu
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        # Add Load action to File menu
        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_file)
        file_menu.addAction(load_action)

    def load_file(self):
        # Open file dialog and load selected data
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", meas_dir,
                                                   "Deposition Data Files (*.dep);;All Files (*)")
        if file_name:
            dep_data = DepositionMeasurements.from_dep(os.path.join(meas_dir, file_name))

            # Update scatter plot with loaded data
            self.plot_widget.update_data_plot(dep_data)
