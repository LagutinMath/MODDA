from PySide6.QtGui import QFont
import pyqtgraph as pg


class MainPlot(pg.PlotWidget):
    def __init__(self, program_data):
        super().__init__()

        self.program_data = program_data

        # Set white background color
        self.setBackground('w')

        # Define styles
        axis_font = QFont('Times New Roman', 16)
        label_style = "<span style='font-size: 16pt; font-family: Times New Roman; color: black;'>{}</span>"
        axis_pen = pg.mkPen(color='black', width=2)

        # Apply styles to axes
        self.set_axis_style('bottom', 'Time (s)', axis_font, axis_pen, label_style)
        self.set_axis_style('left', 'Transmittance (abs)', axis_font, axis_pen, label_style)

        # Initial data plot
        if self.program_data.dep_data is not None:
            self.update_data_plot()

        self.curve = None

        # Add approximation curve corresponding the model
        self.program_data.model_changed.connect(self.update_curve)

    def set_axis_style(self, axis_name, label, font, pen, label_style):
        axis = self.getPlotItem().getAxis(axis_name)
        axis.setPen(pen)
        axis.setTextPen('black')
        axis.setStyle(tickFont=font)
        self.getPlotItem().setLabel(axis_name, label_style.format(label))

    def add_data_plot(self):
        for layer in self.program_data.dep_data.measurements.keys():
            x_data, y_data = self.program_data.dep_data.get_consequent_data(layer)

            if self.program_data.dep_data.design.layer_role(layer) == 'H':
                color = 'blue'
            elif self.program_data.dep_data.design.layer_role(layer) == 'L':
                color = 'red'
            else:
                color = 'black'

            # Create a new ScatterPlotItem for each layer
            scatter = pg.ScatterPlotItem(x=x_data, y=y_data, size=5, pen=pg.mkPen(None), brush=pg.mkBrush(color))
            self.addItem(scatter)

    def update_data_plot(self):
        # Update scatter plot with new data
        self.clear()
        self.add_data_plot()
        # self.add_model_curve()

    # def add_model_curve(self):
    #     x_data, y_data = self.model.get_xy_data(self.dep_data.start_time[1],
    #                                             self.dep_data.final_time[self.dep_data.design.N])
    #     curve = pg.PlotDataItem(x_data, y_data, pen=pg.mkPen(color='black', width=5))
    #     self.addItem(curve)
    #     return curve
    #
    def update_curve(self, kwargs):
        self.program_data.models[0].update(kwargs)
        x_data, y_data = self.program_data.models[0].get_xy_data(self.program_data.dep_data.start_time[1],
                                                self.program_data.dep_data.final_time[self.program_data.dep_data.design.N])
        if self.curve is None:
            self.curve = pg.PlotDataItem(x_data, y_data, pen=pg.mkPen(color='black', width=5))
            self.addItem(self.curve)
        else:
            self.curve.setData(x_data, y_data)
