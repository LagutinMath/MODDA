from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolButton, QLabel, QScrollArea, QPushButton
from PySide6.QtCore import Qt
from modda.data_handler.BaseNonlocalModel import BaseNonlocalModel
from modda.gui.ModelSliders import ModelSliders


class ModelSection(QWidget):
    def __init__(self, program_data):
        super().__init__()

        self.program_data = program_data

        # Create the main layout for the whole section (including button and scroll area)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Add toggle button
        self.toggle_button = self.add_toggle_button()

        # Create the scroll area for the content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create the content container inside the scroll area
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)

        # Add button to add model
        self.new_model_button = self.add_new_model_button()

        # Set the content container as the scroll area's widget
        self.scroll_area.setWidget(self.content_container)

        # Add the scroll area to the main layout
        self.main_layout.addWidget(self.scroll_area)

    def add_new_model_button(self):
        button = QPushButton("Add model")
        self.content_layout.addWidget(button)
        button.clicked.connect(self.add_model)
        return button

    def add_model(self):
        # Load model
        model = BaseNonlocalModel.init_coef(self.program_data.dep_data, 3)
        self.program_data.models.append(model)

        # Add sliders
        sliders = ModelSliders(self.program_data)
        self.content_layout.addWidget(sliders)

        # Hide button after setting model
        self.new_model_button.hide()

    def add_toggle_button(self):
        toggle_button = QToolButton()
        toggle_button.setArrowType(Qt.DownArrow)
        toggle_button.setFixedHeight(10)
        toggle_button.setFixedWidth(100)
        toggle_button.clicked.connect(self.toggle_sections)
        self.main_layout.addWidget(toggle_button, alignment=Qt.AlignTop | Qt.AlignHCenter)
        return toggle_button

    def toggle_sections(self):
        if self.scroll_area.isVisible():
            self.scroll_area.hide()

            # Shrink to button width
            self.setMaximumHeight(self.toggle_button.height())
            self.setMinimumHeight(self.toggle_button.height())

            # Change arrow direction to opposite
            self.toggle_button.setArrowType(Qt.UpArrow)
        else:
            self.scroll_area.show()

            # Allow resizing again
            self.setMaximumHeight(16777215)
            self.setMinimumHeight(0)

            # Change arrow direction to opposite
            self.toggle_button.setArrowType(Qt.DownArrow)
