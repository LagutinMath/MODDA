import sys
from PySide6.QtWidgets import QApplication
from modda.gui.MainWindow import MainWindow
from modda.data_handler.ProgramData import ProgramData


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('MODDA')

    program_data = ProgramData()

    win = MainWindow(program_data)
    win.show()
    app.exec()


if __name__ == '__main__':
    main()
