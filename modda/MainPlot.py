from PySide6.QtGui import QFont
import pyqtgraph as pg
from DepositionMeasurements import DepositionMeasurements
from paths import meas_dir
import os
from BaseNonlocalModel import BaseNonlocalModel


class MainPlot(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        # Set white background color
        self.setBackground('w')

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
        self.add_approx()

    def set_axis_style(self, axis_name, label, font, pen, label_style):
        axis = self.getPlotItem().getAxis(axis_name)
        axis.setPen(pen)
        axis.setTextPen('black')
        axis.setStyle(tickFont=font)
        self.getPlotItem().setLabel(axis_name, label_style.format(label))

    def init_data_plot(self):
        # Load initial data and update scatter plot
        file_name = '24_03-AR_4_Zh.dep'
        dep_data = DepositionMeasurements.from_dep(os.path.join(meas_dir, file_name))
        self.data_plot_from_dep_data(dep_data)

    def data_plot_from_dep_data(self, dep_data):
        for layer in dep_data.measurements.keys():
            x_data, y_data = dep_data.get_consequent_data(layer)

            if dep_data.design.layer_role(layer) == 'H':
                color = 'blue'
            elif dep_data.design.layer_role(layer) == 'L':
                color = 'red'
            else:
                color = 'black'

            # Create a new ScatterPlotItem for each layer
            scatter = pg.ScatterPlotItem(x=x_data, y=y_data, size=5, pen=pg.mkPen(None), brush=pg.mkBrush(color))
            self.addItem(scatter)

    def update_data_plot(self, dep_data):
        # Update scatter plot with new data
        self.clear()
        self.data_plot_from_dep_data(dep_data)

    def add_approx(self):
        file_name = '24_03-AR_4_Zh.dep'
        dep_data = DepositionMeasurements.from_dep(os.path.join(meas_dir, file_name))
        model = BaseNonlocalModel.init_coef(dep_data, 1)
        x_data, y_data = model.get_xy_data(dep_data.start_time[1], dep_data.final_time[1])
        approx_plot = pg.PlotDataItem(x_data, y_data, pen=pg.mkPen(color='black', width=2))
        self.addItem(approx_plot)
