from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QFileDialog)
from PySide6.QtGui import QAction
import pyqtgraph as pg
from DepositionMeasurements import DepositionMeasurements
from paths import meas_dir
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create layout and menu
        self.create_menu()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Initialize plot widget and scatter (to be updated later)
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        # Create scatter plot item but do not set data yet
        self.scatter = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0))
        self.plot_widget.addItem(self.scatter)

        # Initial data plot
        self.create_data_plot()

    def create_data_plot(self):
        # Load initial data and update scatter plot
        file_name = '24_03-AR_4_Zh.dep'
        dep_data = DepositionMeasurements.from_dep(os.path.join(meas_dir, file_name))
        layer = 3
        x_data = dep_data.measurements[layer].t
        y_data = dep_data.measurements[layer].y_data

        # Update scatter plot with data
        self.update_data_plot(x_data, y_data)

    def update_data_plot(self, x_data, y_data):
        # Update scatter plot with new data
        self.scatter.setData(x_data, y_data)

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
            layer = 1
            x_data = dep_data.measurements[layer].t
            y_data = dep_data.measurements[layer].y_data

            # Update scatter plot with loaded data
            self.update_data_plot(x_data, y_data)
