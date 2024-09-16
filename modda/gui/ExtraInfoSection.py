from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QToolButton, QLabel, QScrollArea, QSizePolicy
from PySide6.QtCore import Qt


class ExtraInfoSection(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main layout for the whole section (including button and scroll area)
        self.main_layout = QHBoxLayout(self)
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

        # Example content added to the scroll area
        self.label = QLabel("Test label")
        self.content_layout.addWidget(self.label)

        # Set the content container as the scroll area's widget
        self.scroll_area.setWidget(self.content_container)

        # Add the scroll area to the main layout
        self.main_layout.addWidget(self.scroll_area)

    def add_toggle_button(self):
        toggle_button = QToolButton()
        toggle_button.setArrowType(Qt.RightArrow)
        toggle_button.setFixedHeight(100)
        toggle_button.setFixedWidth(10)
        toggle_button.clicked.connect(self.toggle_sections)
        self.main_layout.addWidget(toggle_button, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        return toggle_button

    def toggle_sections(self):
        if self.scroll_area.isVisible():
            self.scroll_area.hide()

            # Shrink to button width
            self.setMaximumWidth(self.toggle_button.width())
            self.setMinimumWidth(self.toggle_button.width())

            # Change arrow direction to opposite
            self.toggle_button.setArrowType(Qt.LeftArrow)
        else:
            self.scroll_area.show()

            # Allow resizing again
            self.setMaximumWidth(16777215)
            self.setMinimumWidth(0)

            # Change arrow direction to opposite
            self.toggle_button.setArrowType(Qt.RightArrow)
