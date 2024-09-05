from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QFileDialog)
from PySide6.QtGui import QAction, QFont
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

        # Initialize plot widget with white background
        self.plot_widget = pg.PlotWidget(background='w')
        self.layout.addWidget(self.plot_widget)

        # Define styles
        axis_font = QFont('Times New Roman', 16)
        label_style = "<span style='font-size: 16pt; font-family: Times New Roman; color: black;'>{}</span>"
        axis_pen = pg.mkPen(color='black', width=2)

        # Apply styles to axes
        self.set_axis_style('bottom', 'Time (s)', axis_font, axis_pen, label_style)
        self.set_axis_style('left', 'Transmittance (abs)', axis_font, axis_pen, label_style)

        # Create scatter plot item
        # scatter_plots = []
        # self.scatter = pg.ScatterPlotItem(size=5, pen=pg.mkPen(None), brush=pg.mkBrush(0, 0, 200))
        # self.plot_widget.addItem(self.scatter)

        # Initial data plot
        self.init_data_plot()

    def set_axis_style(self, axis_name, label, font, pen, label_style):
        axis = self.plot_widget.getPlotItem().getAxis(axis_name)
        axis.setPen(pen)
        axis.setTextPen('black')
        axis.setStyle(tickFont=font)
        self.plot_widget.getPlotItem().setLabel(axis_name, label_style.format(label))

    def init_data_plot(self):
        # Load initial data and update scatter plot
        file_name = '24_03-AR_4_Zh.dep'
        dep_data = DepositionMeasurements.from_dep(os.path.join(meas_dir, file_name))
        self.data_plot_from_dep_data(dep_data)

    def data_plot_from_dep_data(self, dep_data):
        time_shift = 0
        for layer in dep_data.measurements.keys():
            x_data = dep_data.measurements[layer].t + time_shift
            y_data = dep_data.measurements[layer].y_data
            time_shift = x_data[-1]

            if dep_data.design.layer_role(layer) == 'H':
                color = 'blue'
            elif dep_data.design.layer_role(layer) == 'L':
                color = 'red'
            else:
                color = 'black'

            # Create a new ScatterPlotItem for each layer
            scatter = pg.ScatterPlotItem(x=x_data, y=y_data, size=5, pen=pg.mkPen(None), brush=pg.mkBrush(color))
            self.plot_widget.addItem(scatter)

    def update_data_plot(self, dep_data):
        # Update scatter plot with new data
        self.plot_widget.clear()
        self.data_plot_from_dep_data(dep_data)

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
        self.update_data_plot(dep_data)
