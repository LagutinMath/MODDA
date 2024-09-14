class ProgramData:
    def __init__(self, dep_data=None, model=None):
        self.dep_data = dep_data
        self.model = model

    def update_dep_data(self, dep_data):
        self.dep_data = dep_data
