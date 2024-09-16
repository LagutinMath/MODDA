from PySide6.QtCore import Signal, QObject


class ProgramData(QObject):
    model_changed = Signal(dict)

    def __init__(self, dep_data=None):
        super().__init__()
        self.dep_data = dep_data
        self.models = []

    def update_dep_data(self, dep_data):
        self.dep_data = dep_data
