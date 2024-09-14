from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolButton, QLabel, QScrollArea, QSizePolicy
from PySide6.QtCore import Qt


class ModelSection(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main layout for the whole section (including button and scroll area)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Add toggle button
        self.toggle_button = QToolButton()
        self.toggle_button.setArrowType(Qt.DownArrow)
        self.toggle_button.setFixedHeight(10)
        self.toggle_button.setFixedWidth(100)
        self.toggle_button.clicked.connect(self.toggle_sections)
        self.main_layout.addWidget(self.toggle_button, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Create the scroll area for the content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create the content container inside the scroll area
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)

        # Example content added to the scroll area
        self.label = QLabel("Test label")
        self.content_layout.addWidget(self.label)

        # Set the content container as the scroll area's widget
        self.scroll_area.setWidget(self.content_container)

        # Add the scroll area to the main layout
        self.main_layout.addWidget(self.scroll_area)

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
