import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout)
import pyqtgraph as pg
from DepositionMeasurements import DepositionMeasurements

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = QMainWindow()
    central_widget = QWidget()
    win.setCentralWidget(central_widget)

    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    plot_widget = pg.PlotWidget()
    layout.addWidget(plot_widget)

    # the data load
    file_name = '24_03-AR_4_Zh.dep'
    save_folder = r'C:\Multilayer_optics_data\Measurements'
    file_path = save_folder + '\\' + file_name
    dep_data = DepositionMeasurements.from_dep(file_path)
    layer = 3
    x_data = dep_data.measurements[layer].t
    y_data = dep_data.measurements[layer].y_data

    scatter = pg.ScatterPlotItem(x_data, y_data, size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0))
    plot_widget.addItem(scatter)

    win.show()
    app.exec()
