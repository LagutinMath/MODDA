from PySide6.QtWidgets import QMainWindow, QSplitter
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from modda.gui.MainPlotSection import MainPlotSection
from modda.gui.ModelSection import ModelSection
from modda.gui.ExtraInfoSection import ExtraInfoSection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create menu
        self.create_menu()

        # Create the main splitter for layout
        main_splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(main_splitter)

        # Left-side (main plot and model sections)
        left_splitter = QSplitter(Qt.Vertical)
        main_splitter.addWidget(left_splitter)

        # Main Plot Section
        self.main_plot_section = MainPlotSection()
        left_splitter.addWidget(self.main_plot_section)

        # Model Section (with scroll)
        self.model_section = ModelSection()
        left_splitter.addWidget(self.model_section)

        # Extra Info Section (with scroll)
        self.extra_info_section = ExtraInfoSection()
        main_splitter.addWidget(self.extra_info_section)

    def create_menu(self):
        # Create the menu bar and add File menu
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        # Add Load action to File menu
        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_file)
        file_menu.addAction(load_action)

    def load_file(self):
        pass
